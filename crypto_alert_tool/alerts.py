import smtplib
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Dict
import os 

def send_email(subject: str, message: str, email_config: Dict[str, str], image_path: str = None) -> None:
    """
    Send an email with the given subject, message and optional image attachment.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        email_config (Dict[str, str]): A dictionary containing email configuration.
        image_path (str, optional): Path to the image file to attach.
    """
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = email_config["sender"]
    msg["To"] = email_config["receiver"]
    
    # add text to the msj
    msg.attach(MIMEText(message))
    
    # attach the image if exist
    if image_path:
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(img)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_config["sender"], email_config["password"])
            server.sendmail(email_config["sender"], email_config["receiver"], msg.as_string())
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"Error sending email: {e}")

def send_whatsapp(message: str, whatsapp_config: Dict[str, str]) -> None:
    """
    Send a WhatsApp message with the given message using the provided WhatsApp configuration.

    Args:
        message (str): The body of the WhatsApp message.
        whatsapp_config (Dict[str, str]): A dictionary containing WhatsApp configuration with keys 'account_sid', 'auth_token', 'from_number', and 'to_number'.

    Raises:
        Exception: If there is an error sending the WhatsApp message.
    """
    client = Client(whatsapp_config["account_sid"], whatsapp_config["auth_token"])
    try:
        client.messages.create(
            body=message,
            from_=whatsapp_config["from_number"],
            to=whatsapp_config["to_number"]
        )
    except Exception as e:
        raise Exception(f"Error sending WhatsApp message: {e}")
