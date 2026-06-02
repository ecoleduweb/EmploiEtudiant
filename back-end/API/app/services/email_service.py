import requests
import os
import logging
from msal import ConfidentialClientApplication
from flask import current_app, request

enabled = os.environ.get('MAIL_ENABLED') == "True"
logger = logging.getLogger(__name__)
scopes = ['https://graph.microsoft.com/.default']

def get_microsoft_graph_token():
    """
    Acquires an access token for Microsoft Graph API using client credentials flow.
    
    Returns:
        dict: The token result containing 'access_token' if successful, or error details.
    """
    client_id = os.environ.get('MAIL_CLIENT_ID')
    client_secret = os.environ.get('MAIL_CLIENT_SECRET')
    tenant_id = os.environ.get('MAIL_TENANT_ID')
    
    try:
        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=f"https://login.microsoftonline.com/{tenant_id}"
        )

        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" not in result:
            logger.warning(f"Échec d'obtention du token: {result.get('error')} - {result.get('error_description')}")
        else:
            logger.info("Token Microsoft Graph obtenu avec succès")
            
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'acquisition du token Microsoft Graph: {str(e)}")
        return {"error": "authentication_failed", "error_description": str(e)}

def send_mail(receiver_mail, subject, content):
    """
    Envoie un email via l'API Microsoft Graph.
    
    Args:
        receiver_mail (str): Adresse email du destinataire
        subject (str): Sujet de l'email
        content (str): Contenu de l'email (sera intégré dans un template HTML)
    """
    logger.info(f"Tentative d'envoi de mail à {receiver_mail}")
    
    graph_user_id = os.environ.get('MAIL_GRAPH_USER_ID')
    
    if (not enabled or current_app.config.get('TESTING')):
        logger.info(f"Envoi d'email désactivé: enabled={enabled}, URL={request.url_root}, testing={current_app.config.get('TESTING')}")
        return True # Simule un envoi réussi en mode test ou si l'envoi est désactivé
    
    logger.info("Appel à get_microsoft_graph_token()")
    token_result = get_microsoft_graph_token()
    logger.info(f"Résultat de token obtenu: {'succès' if 'access_token' in token_result else 'échec'}")
    
    if "access_token" in token_result:
        graph_endpoint = f"https://graph.microsoft.com/v1.0/users/{graph_user_id}/sendMail"
        
        formatted_subject = "Site de recrutement - " + subject
        
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
                'subject': formatted_subject,
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
        
        headers = {
            'Authorization': 'Bearer ' + token_result['access_token'],
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(graph_endpoint, headers=headers, json=email_msg)
            if response.status_code == 202:
                logger.info(f"Email envoyé avec succès à {receiver_mail}")
                return True
            else:
                logger.warning(f"Échec de l'envoi d'email: Code {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
            logger.exception("Exception complète:")
            return False
    else:
        logger.warning(f"Impossible d'envoyer l'email: problème d'authentification - {token_result.get('error')}")
        return False