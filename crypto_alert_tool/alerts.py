import smtplib
from twilio.rest import Client
from email.mime.text import MIMEText
from typing import Dict

def send_email(subject: str, message: str, email_config: Dict[str, str]) -> None:
    """
    Send an email with the given subject and message using the provided email configuration.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        email_config (Dict[str, str]): A dictionary containing email configuration with keys 'sender', 'receiver', and 'password'.

    Raises:
        smtplib.SMTPException: If there is an error sending the email.
    """
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = email_config["sender"]
    msg["To"] = email_config["receiver"]

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
