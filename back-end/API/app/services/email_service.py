import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, current_app, request
import os

# Configuration
port = os.environ.get('MAIL_PORT')
smtp_server = os.environ.get('MAIL_SERVER')
sender_email = os.environ.get('MAIL_SENDER')
login = os.environ.get('MAIL_SERVER_LOGIN')
password = os.environ.get('MAIL_SERVER_PASSWORD')

def sendMail(receiver_email, subject, content):
    if (request.url_root.find("http://localhost") == 0 or current_app.config.get('TESTING')): return
    
    subject = "Site de recrutement - " + subject
    html = """\
    <html>
    <body>
    <p>Ce message est automatisé. Merci de ne pas y répondre, car aucune réponse ne sera traitée.</p>
    <hr>
    <p>Bonjour,</p>
    <p>""" + content + """</p>
    <br>
    <hr>
    <img src="https://www.cegeprdl.ca/images/logo-header.png" alt="Logo" width="200" height="40">
    <p>Cégep de Rivière-du-Loup</p>
    <p>80, rue Frontenac, Rivière-du-Loup (Québec) G5R 1R1</p>
    <a href=https://emploietudiant.cegeprdl.ca/>https://emploietudiant.cegeprdl.ca</a>
    </body>
    </html>
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the HTML part
    message.attach(MIMEText(html, "html"))

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.connect(smtp_server, port)
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

    return True
