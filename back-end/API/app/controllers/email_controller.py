import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint
import os

# Configuration
port = os.environ.get('MAIL_PORT')
smtp_server = os.environ.get('MAIL_SERVER')
sender_email = os.environ.get('MAIL_SENDER')
login = os.environ.get('MAIL_SERVER_LOGIN')
password = os.environ.get('MAIL_SERVER_PASSWORD')

def sendMail(receiver_email, subject, content):

    subject = "Site de recrutement - " + subject
    html = """\
    <html>
    <body>
        <p>""" + content + """</p>
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
    print(smtp_server, port, login, password, sender_email, receiver_email)
    with smtplib.SMTP(smtp_server, port) as server:
        server.connect(smtp_server, port)
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    return True