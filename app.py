from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea
from flasf_mail import Mail, Message
from datetime import date, datetime
import socket

# For dev purposes only; delete when deployed
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# Initialize app and contact form
app = Flask(__name__)

class ContactForm(FlaskForm):


@app.route('/', methods=['GET', 'POST'])
def index():
    # contact = ContactForm()

    return render_template("index.html")

# RUN APP
if __name__ == '__main__':
    app.run(debug=True, host=str(IPAddr))