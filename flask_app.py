# standard library imports
import os
import logging
import requests
import json
import time
from datetime import datetime, timedelta

# third-party imports
from flask import Flask, render_template, url_for, redirect, request, send_file, jsonify, flash, session
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
import hashlib


# local imports
from speakers import speakers
from team import team

# ----------------------
# App / Config
# ----------------------

from pathlib import Path
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)


# Initialize app and contact form
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY')
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD') 


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

# Log admin password status
if app.config['ADMIN_PASSWORD'] == 'admin123':
    logger.warning("Using default admin password 'admin123'. Set ADMIN_PASSWORD environment variable for production.")
else:
    logger.info("Admin password configured from environment variable.")

csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.error(f"CSRF failed: {e.description}")
    return jsonify({"success": False, "message": f"CSRF failed: {e.description}"}), 400

# ----------------------
# Admin Authentication
# ----------------------

def hash_password(password):
    """Simple password hashing using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin_password(password):
    """Verify admin password"""
    stored_hash = hash_password(app.config['ADMIN_PASSWORD'])
    input_hash = hash_password(password)
    return stored_hash == input_hash

def send_admin_access_alert(admin_name, ip_address, access_type, success=True):
    """Send email alert for admin login attempts (security-focused)"""
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "SUCCESS" if success else "FAILED"
        
        subject = f"Admin Login Alert - {status} - {admin_name}"
        
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: {'#28a745' if success else '#dc3545'};">
                Admin Login Alert - {status}
            </h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3>Login Details:</h3>
                <p><strong>Admin Name:</strong> {admin_name}</p>
                <p><strong>IP Address:</strong> {ip_address}</p>
                <p><strong>Timestamp:</strong> {current_time}</p>
                <p><strong>Status:</strong> {status}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <p><strong>User Agent:</strong></p>
                <p style="background: #e9ecef; padding: 10px; border-radius: 3px; word-break: break-all;">
                    {request.headers.get('User-Agent', 'Unknown')}
                </p>
            </div>
            
            <div style="background: {'#d4edda' if success else '#f8d7da'}; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 0; color: {'#155724' if success else '#721c24'};">
                    {f'✅ Admin successfully logged in' if success else '❌ Failed admin login attempt'}
                </p>
            </div>
            
            <hr style="margin: 30px 0;">
            <p style="color: #6c757d; font-size: 12px;">
                This is an automated security alert from the Envision AI Website admin system.
                {'You will only receive alerts for login attempts, not for page access.' if success else 'If you did not make this login attempt, please review your security settings immediately.'}
            </p>
        </div>
        """
        
        # Send to the same email as form submissions
        if MAIL_TO:
            send_resend(
                to=MAIL_TO,
                subject=subject,
                html=html,
                reply_to_email="security@envisionprinceton.com",
                reply_to_name="Envision Security System"
            )
            logger.info(f"Admin access alert sent: {admin_name} - {access_type} - {status}")
        
    except Exception as e:
        logger.error(f"Failed to send admin access alert: {e}")

def is_admin_authenticated():
    """Check if user is authenticated as admin"""
    return session.get('admin_authenticated', False)

def require_admin_auth(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            return jsonify({"error": "Authentication required", "login_url": "/admin/login"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

class AdminLoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Your Name"})
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# ----------------------
# Duplicate Submission Prevention
# ----------------------

SUBMISSION_TRACK_FILE = "submission_tracking.json"

def load_submission_tracking():
    """Load submission tracking data from file"""
    try:
        if os.path.exists(SUBMISSION_TRACK_FILE):
            with open(SUBMISSION_TRACK_FILE, 'r') as f:
                data = json.load(f)
                logger.info(f"Loaded tracking data with {len(data)} entries")
                # Clean up old entries (older than 30 days)
                current_time = time.time()
                cleaned_data = {}
                for key, value in data.items():
                    # Check if this is the new format with submissions array
                    if 'submissions' in value:
                        # New format: clean up old submissions within each entry
                        submissions = value.get('submissions', [])
                        recent_submissions = [s for s in submissions if current_time - s['timestamp'] < (30 * 24 * 60 * 60)]
                        
                        # Only keep entries that have recent submissions
                        if recent_submissions:
                            cleaned_value = value.copy()
                            cleaned_value['submissions'] = recent_submissions
                            cleaned_value['last_submission'] = max(s['timestamp'] for s in recent_submissions)
                            cleaned_data[key] = cleaned_value
                    else:
                        # Old format: check timestamp directly (backward compatibility)
                        if 'timestamp' in value and current_time - value['timestamp'] < (30 * 24 * 60 * 60):
                            cleaned_data[key] = value
                logger.info(f"Returning cleaned tracking data with {len(cleaned_data)} entries")
                return cleaned_data
        logger.warning("Tracking file does not exist")
        return {}
    except Exception as e:
        logger.error(f"Error loading submission tracking: {e}")
        return {}

def save_submission_tracking(data):
    """Save submission tracking data to file"""
    try:
        with open(SUBMISSION_TRACK_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving submission tracking: {e}")

def check_duplicate_submission(name, email, ip):
    """
    Check if this submission exceeds the limits:
    - Maximum 4 submissions per 2 weeks (14 days)
    - 24-hour cooldown between every 2 submissions
    Returns (is_duplicate, message) tuple
    """
    tracking_data = load_submission_tracking()
    current_time = time.time()
    
    MAX_SUBMISSIONS = 4
    TWO_WEEKS = 14 * 24 * 60 * 60  # 14 days in seconds
    COOLDOWN_PERIOD = 24 * 60 * 60  # 24 hours in seconds
    
    # normalize inputs for comparison
    normalized_name = name.strip().lower()
    normalized_email = email.strip().lower()
    
    # Check submission limits for name
    if normalized_name in tracking_data:
        name_data = tracking_data[normalized_name]
        submissions = name_data.get('submissions', [])
        
        # clean up old submissions (older than 2 weeks)
        recent_submissions = [s for s in submissions if current_time - s['timestamp'] < TWO_WEEKS]
        
        # Check if max submissions reached
        if len(recent_submissions) >= MAX_SUBMISSIONS:
            oldest_submission = min(recent_submissions, key=lambda x: x['timestamp'])
            time_until_reset = TWO_WEEKS - (current_time - oldest_submission['timestamp'])
            days_until_reset = time_until_reset / (24 * 60 * 60)
            
            logger.warning(f"Submission limit exceeded - name '{name}' has submitted {len(recent_submissions)}/{MAX_SUBMISSIONS} times in the last 2 weeks from IP {ip}")
            return True, f"The name '{name}' has reached the maximum number of submissions ({MAX_SUBMISSIONS}) for this 2-week period. Please wait {days_until_reset:.1f} days before submitting again."
        
        # Check cooldown period (24 hours between every 2 submissions)
        if len(recent_submissions) >= 2:
            # Sort submissions by timestamp (most recent first)
            recent_submissions.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # check if we're in a cooldown period (after every 2nd submission)
            submission_pairs = len(recent_submissions) // 2
            if submission_pairs > 0:
                # check the most recent pair
                last_pair_start = recent_submissions[submission_pairs * 2 - 1]['timestamp']
                time_since_last_pair = current_time - last_pair_start
                
                if time_since_last_pair < COOLDOWN_PERIOD:
                    time_until_cooldown_ends = COOLDOWN_PERIOD - time_since_last_pair
                    hours_until_cooldown_ends = time_until_cooldown_ends / 3600
                    
                    logger.warning(f"Cooldown period active - name '{name}' submitted {len(recent_submissions)} times, cooldown ends in {hours_until_cooldown_ends:.1f} hours from IP {ip}")
                    return True, f"Please wait {hours_until_cooldown_ends:.1f} hours before submitting again. There is a 24-hour cooldown period after every 2 submissions."
    
    # Check submission limits for email (same logic)
    if normalized_email in tracking_data:
        email_data = tracking_data[normalized_email]
        submissions = email_data.get('submissions', [])
        
        # Clean up old submissions (older than 2 weeks)
        recent_submissions = [s for s in submissions if current_time - s['timestamp'] < TWO_WEEKS]
        
        # Check if max submissions reached
        if len(recent_submissions) >= MAX_SUBMISSIONS:
            oldest_submission = min(recent_submissions, key=lambda x: x['timestamp'])
            time_until_reset = TWO_WEEKS - (current_time - oldest_submission['timestamp'])
            days_until_reset = time_until_reset / (24 * 60 * 60)
            
            logger.warning(f"Submission limit exceeded - email '{email}' has submitted {len(recent_submissions)}/{MAX_SUBMISSIONS} times in the last 2 weeks from IP {ip}")
            return True, f"The email '{email}' has reached the maximum number of submissions ({MAX_SUBMISSIONS}) for this 2-week period. Please wait {days_until_reset:.1f} days before submitting again."
        
        # Check cooldown period (24 hours between every 2 submissions)
        if len(recent_submissions) >= 2:
            # Sort submissions by timestamp (most recent first)
            recent_submissions.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Check if we're in a cooldown period (after every 2nd submission)
            submission_pairs = len(recent_submissions) // 2
            if submission_pairs > 0:
                # Check the most recent pair
                last_pair_start = recent_submissions[submission_pairs * 2 - 1]['timestamp']
                time_since_last_pair = current_time - last_pair_start
                
                if time_since_last_pair < COOLDOWN_PERIOD:
                    time_until_cooldown_ends = COOLDOWN_PERIOD - time_since_last_pair
                    hours_until_cooldown_ends = time_until_cooldown_ends / 3600
                    
                    logger.warning(f"Cooldown period active - email '{email}' submitted {len(recent_submissions)} times, cooldown ends in {hours_until_cooldown_ends:.1f} hours from IP {ip}")
                    return True, f"Please wait {hours_until_cooldown_ends:.1f} hours before submitting again. There is a 24-hour cooldown period after every 2 submissions."
    
    # Record this submission
    submission_record = {
        'timestamp': current_time,
        'ip': ip,
        'name': name,
        'email': email
    }
    
    # update tracking data for name
    if normalized_name in tracking_data:
        tracking_data[normalized_name]['submissions'].append(submission_record)
        tracking_data[normalized_name]['last_submission'] = current_time
        tracking_data[normalized_name]['last_ip'] = ip
    else:
        tracking_data[normalized_name] = {
            'submissions': [submission_record],
            'first_submission': current_time,
            'last_submission': current_time,
            'last_ip': ip,
            'email': normalized_email,
            'name': name
        }
    
    # update tracking data for email
    if normalized_email in tracking_data:
        tracking_data[normalized_email]['submissions'].append(submission_record)
        tracking_data[normalized_email]['last_submission'] = current_time
        tracking_data[normalized_email]['last_ip'] = ip
    else:
        tracking_data[normalized_email] = {
            'submissions': [submission_record],
            'first_submission': current_time,
            'last_submission': current_time,
            'last_ip': ip,
            'name': normalized_name,
            'email': email
        }
    
    save_submission_tracking(tracking_data)
    
    # Log successful submission with count info
    name_submissions = len([s for s in tracking_data[normalized_name]['submissions'] if current_time - s['timestamp'] < TWO_WEEKS])
    logger.info(f"Submission recorded - name '{name}' (submission #{name_submissions}/{MAX_SUBMISSIONS} in last 2 weeks) from IP {ip}")
    
    return False, None

def real_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

limiter = Limiter(
    key_func=real_ip,
    app=app,
)

# ----------------------
# Mail 
# ----------------------

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
    """
    Verify reCAPTCHA v2 token with Google's API.
    
    Args:
        token (str): The reCAPTCHA response token from the client
        remote_ip (str, optional): The user's IP address
        
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    secret = app.config.get('RECAPTCHA_SECRET_KEY')
    if not secret:
        logger.error("RECAPTCHA_SECRET_KEY is not set.")
        return False, "reCAPTCHA configuration error"

    if not token:
        logger.warning("reCAPTCHA verification attempted with empty token")
        return False, "reCAPTCHA token is missing"

    client_ip = remote_ip or real_ip()
    logger.info("Verifying reCAPTCHA: ip=%s token_len=%s", client_ip, len(token))

    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                'secret': secret,
                'response': token,
                'remoteip': client_ip,
            },
            timeout=10  # Increased timeout for better reliability
        )
        logger.info("reCAPTCHA API response: HTTP %s", resp.status_code)

        if resp.status_code != 200:
            logger.error("reCAPTCHA API non-200 response: %s", resp.text[:200])
            return False, "reCAPTCHA service temporarily unavailable"

        data = resp.json()
        logger.info("reCAPTCHA verification response: %s", data)
        
        success = bool(data.get('success'))
        
        if not success:
            error_codes = data.get('error-codes', [])
            error_messages = []
            
            for error_code in error_codes:
                if error_code == 'missing-input-secret':
                    error_messages.append("reCAPTCHA secret key is missing")
                elif error_code == 'invalid-input-secret':
                    error_messages.append("reCAPTCHA secret key is invalid")
                elif error_code == 'missing-input-response':
                    error_messages.append("reCAPTCHA response is missing")
                elif error_code == 'invalid-input-response':
                    error_messages.append("reCAPTCHA response is invalid")
                elif error_code == 'bad-request':
                    error_messages.append("reCAPTCHA request is malformed")
                elif error_code == 'timeout-or-duplicate':
                    error_messages.append("reCAPTCHA response has expired or been used")
                else:
                    error_messages.append(f"reCAPTCHA error: {error_code}")
            
            error_message = "; ".join(error_messages) if error_messages else "reCAPTCHA verification failed"
            logger.warning("reCAPTCHA verification failed: %s", error_message)
            return False, error_message
        
        logger.info("reCAPTCHA verification successful")
        return True, None

    except RequestException as e:
        logger.exception("reCAPTCHA API request failed: %s", str(e))
        return False, "reCAPTCHA service temporarily unavailable"
    except ValueError as e:
        logger.exception("reCAPTCHA API returned invalid JSON: %s", str(e))
        return False, "reCAPTCHA service error"
    except Exception as e:
        logger.exception("Unexpected error during reCAPTCHA verification: %s", str(e))
        return False, "reCAPTCHA verification error"

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
@limiter.limit("5 per minute") 
def get_involved():
    ip = real_ip()
    # get token sent by reCAPTCHA
    token = request.form.get('g-recaptcha-response', '')
    logger.info("POST /get-involved from %s; token_present=%s; user_agent=%s", 
                ip, bool(token), request.headers.get('User-Agent', 'Unknown')[:100])

    # verify reCAPTCHA
    recaptcha_success, recaptcha_error = verify_recaptcha_v2(token, ip)
    if not recaptcha_success:
        logger.warning("reCAPTCHA verification failed for IP %s: %s", ip, recaptcha_error)
        return jsonify({
            "success": False,
            "message": f"reCAPTCHA verification failed: {recaptcha_error}. Please try again."
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

    # Check for duplicate submissions
    is_duplicate, duplicate_message = check_duplicate_submission(name, email, ip)
    if is_duplicate:
        logger.warning("Duplicate submission blocked: name=%s, email=%s, ip=%s", name, email, ip)
        return jsonify({
            "success": False,
            "message": duplicate_message
        }), 400

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


# ----------------------
# Admin
# ----------------------

@app.route("/admin", methods=['GET'])
def admin_redirect():
    """
    Redirect /admin to /admin/login
    """
    return redirect('/admin/login')

@limiter.limit("3 per minute") 
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    """
    Admin login route
    """
    form = AdminLoginForm()
    
    if request.method == 'GET':
        # Return simple login form HTML with Flask-WTF CSRF token
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login - Envision</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }}
                .form-group {{ margin-bottom: 15px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="text"], input[type="password"] {{ 
                    width: 100%; 
                    padding: 10px; 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    box-sizing: border-box;
                    font-size: 14px;
                }}
                input:focus {{ outline: none; border-color: #007bff; box-shadow: 0 0 5px rgba(0,123,255,0.3); }}
                button {{ 
                    background: #007bff; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    font-size: 16px;
                    width: 100%;
                }}
                button:hover {{ background: #0056b3; }}
                .error {{ color: red; margin-top: 10px; text-align: center; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .header h2 {{ color: #333; margin-bottom: 5px; }}
                .header p {{ color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Admin Login</h2>
                <p>Envision AI Website Administration</p>
            </div>
            <form method="POST">
                {form.csrf_token()}
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" placeholder="Enter your name" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <div id="error" class="error" style="display: none;"></div>
            <script>
                const urlParams = new URLSearchParams(window.location.search);
                if (urlParams.get('error')) {{
                    document.getElementById('error').textContent = urlParams.get('error');
                    document.getElementById('error').style.display = 'block';
                }}
            </script>
        </body>
        </html>
        """
    
    # POST request - handle login
    if form.validate_on_submit():
        name = form.name.data.strip()
        password = form.password.data
        ip = real_ip()
        
        if verify_admin_password(password):
            session['admin_authenticated'] = True
            session['admin_name'] = name
            logger.info(f"Admin login successful: {name} from IP {ip}")
            
            # Send successful login alert
            send_admin_access_alert(name, ip, "LOGIN", success=True)
            
            return redirect('/admin/submissions')
        else:
            logger.warning(f"Failed admin login attempt: {name} from IP {ip}")
            
            # Send failed login alert
            send_admin_access_alert(name, ip, "LOGIN", success=False)
            
            return redirect('/admin/login?error=Invalid password')
    else:
        # Form validation failed (likely CSRF token issue)
        ip = real_ip()
        logger.warning(f"Admin login form validation failed from IP {ip}: {form.errors}")
        return redirect('/admin/login?error=Form validation failed. Please try again.')

@app.route("/admin/logout", methods=['POST'])
def admin_logout():
    """
    Admin logout route
    """
    form = AdminLoginForm()
    ip = real_ip()
    admin_name = session.get('admin_name', 'Unknown')
    
    if form.validate_on_submit():
        session.pop('admin_authenticated', None)
        session.pop('admin_name', None)
        logger.info(f"Admin logout: {admin_name} from IP {ip}")
        
        return redirect('/admin/login')
    else:
        # CSRF validation failed, but we can still allow logout for security
        session.pop('admin_authenticated', None)
        session.pop('admin_name', None)
        logger.warning(f"Admin logout with CSRF validation failed: {admin_name} from IP {ip}")
        
        return redirect('/admin/login')

@app.route("/admin/rate-limit", methods=['GET'])
@require_admin_auth
def view_rate_limiting():
    """
    Admin route to view submission rate limiting data 
    """
    try:
        admin_name = session.get('admin_name', 'Unknown')
        tracking_data = load_submission_tracking()
        current_time = time.time()
        TWO_WEEKS = 14 * 24 * 60 * 60  # 14 days in seconds
        
        # Debug logging
        logger.info(f"Admin dashboard - tracking_data keys: {list(tracking_data.keys())}")
        logger.info(f"Admin dashboard - total entries: {len(tracking_data)}")
        
        # Format data for display
        formatted_data = []
        for key, value in tracking_data.items():
            # Get recent submissions (within 2 weeks)
            submissions = value.get('submissions', [])
            recent_submissions = [s for s in submissions if current_time - s['timestamp'] < TWO_WEEKS]
            
            # Calculate cooldown status
            cooldown_status = "None"
            if len(recent_submissions) >= 2:
                recent_submissions.sort(key=lambda x: x['timestamp'], reverse=True)
                submission_pairs = len(recent_submissions) // 2
                if submission_pairs > 0:
                    last_pair_start = recent_submissions[submission_pairs * 2 - 1]['timestamp']
                    time_since_last_pair = current_time - last_pair_start
                    cooldown_period = 24 * 60 * 60  # 24 hours
                    
                    if time_since_last_pair < cooldown_period:
                        time_until_cooldown_ends = cooldown_period - time_since_last_pair
                        hours_until_cooldown_ends = time_until_cooldown_ends / 3600
                        cooldown_status = f"Active ({hours_until_cooldown_ends:.1f}h remaining)"
                    else:
                        cooldown_status = "Available"
            
            # Format submission history
            submission_history = []
            for submission in sorted(recent_submissions, key=lambda x: x['timestamp'], reverse=True):
                submission_history.append({
                    'timestamp': datetime.fromtimestamp(submission['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    'ip': submission.get('ip', 'N/A'),
                    'hours_ago': f"{(current_time - submission['timestamp']) / 3600:.1f}"
                })
            
            time_diff = current_time - value.get('last_submission', current_time)
            hours_ago = time_diff / 3600
            
            formatted_data.append({
                'identifier': key,
                'name': value.get('name', 'N/A'),
                'email': value.get('email', 'N/A'),
                'total_submissions': len(recent_submissions),
                'max_submissions': 4,
                'cooldown_status': cooldown_status,
                'last_submission': datetime.fromtimestamp(value.get('last_submission', current_time)).strftime('%Y-%m-%d %H:%M:%S'),
                'last_ip': value.get('last_ip', 'N/A'),
                'hours_since_last': f"{hours_ago:.1f}",
                'submission_history': submission_history
            })
        
        # Sort by last submission time (most recent first)
        formatted_data.sort(key=lambda x: x['last_submission'], reverse=True)
        
        # Debug logging
        logger.info(f"Admin dashboard - formatted_data entries: {len(formatted_data)}")
        
        # Create logout form for CSRF token
        logout_form = AdminLoginForm()
        
        return render_template('admin_tracking.html',
                             admin_name=admin_name,
                             tracking_data=tracking_data,
                             formatted_data=formatted_data,
                             csrf_token=logout_form.csrf_token(),
                             active_page='tracking')
    except Exception as e:
        logger.error(f"Error retrieving submission data: {e}")
        return jsonify({"error": "Failed to retrieve submission data"}), 500

@app.route("/admin/submissions", methods=['GET'])
@require_admin_auth
def view_all_submissions():
    """
    Admin route to view all accepted form submissions with complete information
    """
    try:
        admin_name = session.get('admin_name', 'Unknown')
        # Read responses.txt file
        submissions = []
        try:
            with open("responses.txt", "r") as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if line and "\t" in line:
                        parts = line.split("\t")
                        if len(parts) >= 5:
                            submission = {
                                'line_number': line_num,
                                'name': parts[0],
                                'email': parts[1],
                                'affiliation': parts[2],
                                'role': parts[3],
                                'message': parts[4] if len(parts) > 4 else '',
                                'submission_time': 'Unknown'  # responses.txt doesn't store timestamps
                            }
                            submissions.append(submission)
        except FileNotFoundError:
            logger.warning("responses.txt file not found")
        except Exception as e:
            logger.error(f"Error reading responses.txt: {e}")
        
        # Sort submissions by line number (most recent first)
        submissions.sort(key=lambda x: x['line_number'], reverse=True)
        
        # Create logout form for CSRF token
        logout_form = AdminLoginForm()
        
        # Count submissions by role
        role_counts = {}
        for submission in submissions:
            role = submission['role']
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return render_template('admin_submissions.html',
                             admin_name=admin_name,
                             submissions=submissions,
                             role_counts=role_counts,
                             current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             csrf_token=logout_form.csrf_token(),
                             active_page='submissions')
    except Exception as e:
        logger.error(f"Error retrieving all submissions: {e}")
        return jsonify({"error": "Failed to retrieve submissions"}), 500

# RUN APP
if __name__ == '__main__':
    app.run( debug=True, host="127.0.0.1", port=5002)