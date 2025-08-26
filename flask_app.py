# standard library imports
import os
import logging
import requests

# third-party imports
from flask import Flask, render_template, url_for, redirect, request, send_file, jsonify, flash
from flask_wtf import FlaskForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Length, Email
from wtforms.widgets import TextArea
# from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect, CSRFError
from dotenv import load_dotenv
import resend
from resend.exceptions import ResendError
from requests.exceptions import RequestException
from html import escape


# local imports
from speakers import speakers
from team import team

# ----------------------
# App / Config
# ----------------------

load_dotenv()

# Initialize app and contact form
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_APP')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY')
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')

resend.api_key = os.getenv('RESEND_API_KEY')
MAIL_TO = os.getenv('MAIL_TO')
MAIL_FROM = os.getenv('MAIL_FROM')

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger("envision")

if not resend.api_key:
    logger.error("RESEND_API_KEY is not set")
if not MAIL_FROM:
    logger.error("MAIL_FROM is not set (e.g. 'Your App <noreply@verified-domain.com>')")
if not MAIL_TO:
    logger.error("MAIL_TO is not set")

csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.error(f"CSRF failed: {e.description}")
    return jsonify({"success": False, "message": f"CSRF failed: {e.description}"}), 400

def real_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

limiter = Limiter(
    key_func=real_ip,
    app=app,
)

# ----------------------
# Mail 
# ----------------------

# sanity checks after you load env vars
resend.api_key = os.getenv('RESEND_API_KEY')
MAIL_TO = os.getenv('MAIL_TO')
MAIL_FROM = os.getenv('MAIL_FROM')

if not resend.api_key:
    logger.error("RESEND_API_KEY is not set")
if not MAIL_FROM:
    logger.error("MAIL_FROM is not set (e.g. 'Your App <noreply@verified-domain.com>')")
if not MAIL_TO:
    logger.error("MAIL_TO is not set")

class EmailSendError(Exception):
    pass

def _format_reply_to(email, name):
    if not email:
        return None
    return f"{name} <{email}>" if name else email


def send_resend(to, subject, html, reply_to_email=None, reply_to_name=None, bcc=None):
    """
    Sends an email via Resend and returns the message id.
    Raises EmailSendError on failure with detailed context.
    """
    # normalize/validate
    if isinstance(to, (list, tuple, set)):
        to_list = [x.strip() for x in to if x and str(x).strip()]
    else:
        to_list = [str(to).strip()] if to else []
    if not to_list:
        raise ValueError("`to` must not be empty")
    if not subject:
        raise ValueError("`subject` must not be empty")
    if not html:
        raise ValueError("`html` must not be empty")
    if not MAIL_TO:
        raise ValueError("MAIL_TO is not configured")

    # build payload
    payload = {
        "from": "Envision Conference Team <no-reply@envisionprinceton.com>",
        "to": to_list,
        "subject": subject,
        "html": html,
    }

    # add optional fields to payload
    rt = _format_reply_to(reply_to_email, reply_to_name)
    if rt:
        payload["reply_to"] = rt  
    if bcc:
        if isinstance(bcc, (list, tuple, set)):
            bcc_list = [x.strip() for x in bcc if x and str(x).strip()]
        else:
            bcc_list = [str(bcc).strip()]
        if bcc_list:
            payload["bcc"] = bcc_list
    
    # send email
    try:
        resp = resend.Emails.send(payload)  # SDK returns a dict, e.g. {"id": "..."}
    except ResendError as e:
        status = getattr(e, "status_code", None) or getattr(e, "status", None)
        body = getattr(e, "body", None) or getattr(e, "message", None) or str(e)
        logger.error(
            "ResendError sending email: status=%s body=%r payload_keys=%s",
            status, body, list(payload.keys())
        )
        raise EmailSendError("Resend send failed: status=%s body=%r" % (status, body)) from e
    except Exception as e:
        logger.exception("Unexpected exception from Resend SDK")
        raise EmailSendError("Unexpected error: %s" % e) from e

    # extract message id robustly
    msg_id = None
    if isinstance(resp, dict):
        msg_id = resp.get("id")
    else:
        msg_id = getattr(resp, "id", None)

    if not msg_id:
        logger.error("Unexpected Resend response: %r", resp)
        raise EmailSendError("Unexpected response from Resend: %r" % (resp,))

    logger.info("Resend accepted message id=%s to=%s subject=%s", msg_id, to_list, subject)
    return msg_id

# ----------------------
# reCAPTCHA
# ----------------------

def verify_recaptcha_v2(token, remote_ip=None):
    secret = app.config.get('RECAPTCHA_SECRET_KEY')
    if not secret:
        logger.error("RECAPTCHA_SECRET_KEY is not set.")
        return False

    logger.info("Verifying reCAPTCHA: ip=%s token_len=%s", remote_ip or real_ip(), len(token or ""))

    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                'secret': secret,
                'response': token or '',
                'remoteip': remote_ip or real_ip(),
            },
            timeout=5
        )
        logger.info("siteverify HTTP %s", resp.status_code)

        if resp.status_code != 200:
            logger.error("siteverify non-200: %s", resp.text[:200])
            return False

        data = resp.json()
        logger.info("siteverify JSON: %s", data)   # <-- this is the line you want to see
        return bool(data.get('success'))

    except RequestException:
        logger.exception("siteverify request failed")
        return False
    except ValueError:
        logger.exception("siteverify returned non-JSON")
        return False

# ----------------------
# Form
# ----------------------

class ContactForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=2, max=80)], render_kw={"placeholder": "Full Name"})
    email_id = StringField(validators=[InputRequired(), Email(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    affiliation = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Affiliation"})
    role = SelectField(
        "Role",
        choices=[
            ('', 'Please Select a Role'),
            ('speaker', 'Speaker'),
            ('volunteer', 'Volunteer'),
            ('attendee', 'Attendee'),
            ('partner-sponsor', 'Partner / Sponsor'),
        ],
        validators=[InputRequired()],
    )
    message = StringField(validators=[InputRequired(), Length(min=4, max=800)], render_kw={"placeholder": "Enter your message here..."}, widget=TextArea())

    honeypot = HiddenField("website", render_kw={"style": "display: none;"})
    submit = SubmitField("Submit")

# ----------------------
# Routes
# ----------------------

@app.route('/get-involved', methods=['POST'])
@limiter.limit("10 per minute")
def get_involved():
    ip = real_ip()
    # get token sent by reCAPTCHA
    token = request.form.get('g-recaptcha-response', '')
    logger.info("POST /get-involved from %s; token_present=%s", ip, bool(token))

    # verify reCAPTCHA
    if not token or not verify_recaptcha_v2(token, ip):
        return jsonify({
            "success": False,
            "message": "reCAPTCHA verification failed. Please try again."
        }), 400

    print("Form submission received")
    form = ContactForm()

    # form validation failure
    if not form.validate_on_submit():
        return jsonify({
        "success": False, 
        "message": "Form validation failed, please check fields and try again.", 
        "errors": form.errors
        }), 400
    
    # extract form data + sanitize
    name = (form.name.data or "").strip()
    email = (form.email_id.data or "").strip()
    affiliation = (form.affiliation.data or "").strip()
    role = (form.role.data or "").strip()
    message = (form.message.data or "").strip()

    safe_name = escape(name or "")
    safe_email = escape(email or "")
    safe_affiliation = escape(affiliation or "")
    safe_role = escape(role or "")
    safe_message = escape(message or "")
    safe_ip = escape(ip or "")

    if any(x in (name + email) for x in ("\r", "\n")):
        return jsonify({"success": False, "message": "Invalid input."}), 400

    # append to responses.txt for logging
    try:
        with open("responses.txt", "a") as file:
            file.write("\t".join([name, email, affiliation, role, message]) + "\n")
    except Exception as e:
        logger.exception("Failed to write to responses.txt: %s", e)

    # build email
    custom_message = ""
    if safe_role == "speaker":
        custom_message = "<span>Our team will review your submission and reach out to you with more details about speaking at Envision.</span>"
    elif safe_role == "volunteer":
        custom_message = "<span>Our team will review your submission and reach out to you with more details about volunteering at Envision.</span>"
    elif safe_role == "attendee":
        custom_message = "<span>We look forward to seeing you at Envision! Stay tuned for more details soon.</span>"
    elif safe_role == "partner-sponsor":
        custom_message = "<span>Our team will review your submission and reach out to you with more details about partnering or sponsoring Envision.</span>"

    html = f"""
    <div style="text-align:center, width:100%">
        <h3>Thanks for Getting Involved with Envision @ Princeton University.</h3>
        <p>Hi {safe_name},</p>
        <p>Thank you for filling out the Get Involved form for the <b>Envision 2026</b> conference.
        {custom_message}
        Here are the details we received:</p>
        <hr>
        <p><b>Name:</b> {safe_name}</p>
        <p style="text-decoration:none; color:inherit; cursor:text; pointer-events:none;"><b>Email:</b> {safe_email}</p>
        <p><b>Affiliation:</b> {safe_affiliation}</p>
        <p><b>Role:</b> {safe_role if safe_role != "partner-sponsor" else "Partner / Sponsor"}</p>    
        <p><b>Message:</b></p>
        <div style="white-space:pre-wrap">{safe_message}</div>
        <hr>
        
        <p>Envision is Princeton’s annual AI policy and governance conference, bringing together students, researchers, and leaders from around the world. We’re excited you’re interested in being part of it!</p>
        <p>If you have any questions, feel free to reach us at contact@envisionprinceton.com.</p>

        <br><p>Best regards,<br>The Envision Planning Team</p>
    </div>
    <hr>
    <p style="font-size:small;color:gray;">This email was sent to {safe_email} from a form filled out on www.envisionprinceton.com. If you did not fill out the form, please ignore this email.</p>
    """

    # send confirmation email
    subject = f"Envision Get Involved: {safe_name} [{safe_role}]"
    try:
        msg_id = send_resend(
            to= safe_email,
            subject=subject,
            html=html,
            reply_to_email="mpinero@princeton.edu",
            reply_to_name="Envision Planning Team",
            bcc = MAIL_TO 
        )
        
        logger.info("Email sent successfully, message id: %s", msg_id)
    
    except EmailSendError as e:
        logger.exception("EmailSendError: %s", e)
        return jsonify({"success": False, "message": "Email service error, please try again."}), 500

    return jsonify({"success": True, "message": "Form submitted successfully!"})
    

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    return render_template(
        "index.html",
        recaptcha_site_key= app.config['RECAPTCHA_SITE_KEY'],
        ContactForm = form,
        formOff=0,
        speakers=speakers,
        team=team,
        length_team=len(team),
        length_speakers=len(speakers),
        team_slides=int((len(team) / 6) + 0.5) + 1,
        registrationOpen = False  # Set to True if registration is open
    )

''''
@app.route("/noForm", methods=['GET', 'POST'])
def noForm():
    form = ContactForm()
    return render_template(
        "index.html", 
        ContactForm=form, 
        formOff=1,
        speakers=speakers,
        team=team,
        length_team=len(team),
        length_speakers=len(speakers),
        team_slides=int((len(team) / 6) + 0.5) + 1
    )       
'''

@app.route("/schedule", methods=['GET'])
def showSchedule():
    return send_file('templates/EnvisionSchedule.pdf')

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)   