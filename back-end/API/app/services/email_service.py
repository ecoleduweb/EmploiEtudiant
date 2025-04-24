import requests
import os
from msal import ConfidentialClientApplication
from flask import current_app, request

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('MAIL_CLIENT_SECRET')
tenant_id = os.environ.get('MAIL_TENANT_ID')
graph_user_id = os.environ.get('MAIL_GRAPH_USER_ID')
enabled = os.environ.get('MAIL_ENABLED') == "True"

# Initialiser l'application
app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=f"https://login.microsoftonline.com/{tenant_id}"
)

# Obtenir un token pour l'API Graph
scopes = ['https://graph.microsoft.com/.default']
# scopes = ["https://graph.microsoft.com/Mail.Send"]
result = app.acquire_token_for_client(scopes=scopes)
def sendMail(receiver_mail, subject, content):
    # Fonction pour envoyer un email via l'API Graph
    # email = "
    if (not enabled or request.url_root.find("http://localhost") == 0 or current_app.config.get('TESTING')):
        return
    if "access_token" in result:
        # Mettre empetucg dans le .env.... en fait il est déjà la.
        graph_endpoint = f"https://graph.microsoft.com/v1.0/users/{graph_user_id}/sendMail"

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

        email_msg = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': "HTML",
                    'content': html
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': receiver_mail
                        }
                    }
                ]
            }
        }
        print(email_msg)
        headers = {
            'Authorization': 'Bearer ' + result['access_token'],
            'Content-Type': 'application/json'
        }
        
        response = requests.post(graph_endpoint, headers=headers, json=email_msg)
        
        if response.status_code == 202:
            print("Email envoyé avec succès!")
        else:
            print(f"Erreur lors de l'envoi de l'email: {response.status_code}")
            print(response.text)
    else:
        print(result.get("error"))
        print(result.get("error_description"))