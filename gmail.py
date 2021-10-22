import os
import smtplib
import ssl
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from glob import glob
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

def email_with_attachment(header: str, recipient: list, body: str, attachments: list) -> None:
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"

  from_email = os.getenv("EMAIL_ID")
  email_password = os.getenv("EMAIL_PASSWORD")

  message = MIMEMultipart()
  message['From'] = from_email
  message['To'] = email_password
  message['Subject'] = Header(header, 'utf-8')

  if(attachments is not None):

    message.attach(MIMEText(body, 'plain', 'utf-8'))

    for attachment in attachments:
        attachment = open(attachment, 'rb')
        attachment_name = os.path.basename(str(attachment.name))

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachement; filename={}'.format(attachment_name))
        message.attach(part)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(from_email, email_password)
    server.sendmail(from_email, recipient, message.as_string())


if __name__ == '__main__':

  to_email = os.getenv("TO_EMAIL").split(';')
  attachments = glob('data/*.csv')
  
  email_with_attachment(header='header...', recipient=to_email, body='body...', attachments=attachments)
