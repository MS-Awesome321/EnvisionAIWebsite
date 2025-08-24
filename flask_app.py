# standard library imports
import os
import logging

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
import requests

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

csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.error(f"CSRF failed: {e.description}")
    return jsonify({"success": False, "message": f"CSRF failed: {e.description}"}), 400

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger("envision")

def real_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

limiter = Limiter(
    key_func=real_ip,
    app=app,
)
# ----------------------
# RECAPTCHA
# ----------------------

from requests.exceptions import RequestException

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

# # MAIL MANAGER
# app.config['MAIL_SERVER'] = "smtp.gmail.com"
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = '' # Fill this in later
# app.config['MAIL_PASSWORD'] = '' # Fill this in later
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

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

    # verify the token with Google
    if not token or not verify_recaptcha_v2(token, ip):
        return jsonify({
            "success": False,
            "message": "reCAPTCHA verification failed. Please try again."
        }), 400

    print("Form submission received")
    form = ContactForm()
    if form.validate_on_submit():
        if (form.name.data):
            # body = ""
            # for x in [contact.name, contact.email_id, contact.message]:
            #     body = body+(x.data)+"\n"
            # msg = Message(
            #     recipients=["mayanksg2006@gmail.com"],
            #     subject="Entry to Envision Webpage Contact Form",
            #     body=body,
            #     sender="takeaction.club000@gmail.com"
            # )
            # mail.send(msg)
            with open("responses.txt", "a") as file:
                new_entry = ""
                for x in [form.name, form.email_id, form.affiliation, form.role, form.message]:
                    new_entry += (x.data) + "\t"

                file.write(new_entry + "\n")
        return jsonify({"success": True, "message": "Form submitted successfully!"})
    return jsonify({
        "success": False, 
        "message": "Form validation failed, please check fields and try again.", 
        "errors": form.errors
        }), 400

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