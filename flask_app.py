from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from datetime import date, datetime
import socket

# For dev purposes only; delete when deployed
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# Initialize app and contact form
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nHFv%^&NcfDSww@236567H'
csrf = CSRFProtect(app)

# MAIL MANAGER
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '' # Fill this in later
app.config['MAIL_PASSWORD'] = '' # Fill this in later
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Full Name"})
    email_id = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email ID"})
    message = StringField(validators=[InputRequired(), Length(min=4, max=800)], render_kw={"placeholder": "Enter your message here..."}, widget=TextArea())
    submit = SubmitField("Send")

@app.route('/', methods=['GET', 'POST'])
def index():
    contact = ContactForm()

    if contact.validate_on_submit():
        if (contact.name):
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
                for x in [contact.name, contact.email_id, contact.message]:
                    new_entry = new_entry+(x.data)+"\t"
                
                file.write(new_entry+"\n")
            return redirect(url_for("noForm", _anchor='page4'))

    return render_template("index.html", contact=contact, formOff=0)

@app.route("/noForm", methods=['GET', 'POST'])
def noForm():
    contact = ContactForm()
    return render_template("index.html", contact=contact, formOff=1)

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)