from flask import Flask, render_template, url_for, redirect, request, send_file, jsonify
from flask_wtf import FlaskForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea
# from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from speakers import speakers
from team import team


# Initialize app and contact form
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nHFv%^&NcfDSww@236567H'
csrf = CSRFProtect(app)

def real_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

limiter = Limiter(
    key_func=real_ip,
    app=app,
)

# # MAIL MANAGER
# app.config['MAIL_SERVER'] = "smtp.gmail.com"
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = '' # Fill this in later
# app.config['MAIL_PASSWORD'] = '' # Fill this in later
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Full Name"})
    email_id = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
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

@app.route('/get-involved', methods=['POST'])
@limiter.limit("1 per minute")
def get_involved():
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
    return jsonify({"success": False, "message": "Form validation failed", "errors": form.errors})

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    return render_template(
        "index.html",
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