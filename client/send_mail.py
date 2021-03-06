import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import ssl
import magic
import os

import info

def create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Cc'] = cc_addrs
    msg['Date'] = formatdate()
    return msg

def attach_file(msg, attach_dir):
    for file_name in os.listdir(attach_dir):
        path = os.path.join(attach_dir, file_name)
        with open(path, 'rb') as fp:
            types = get_mimetypes(path)
            attachment = MIMEBase(types['maintype'], types['subtype'])
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition', 'attachment',
                filename = file_name
            )
            msg.attach(attachment)

def add_text(msg, body):
    msg.attach(MIMEText(body))

def send_mail(from_addr, to_addrs, password, msg):
    sender = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    sender.login(from_addr, password)
    sender.sendmail(from_addr, to_addrs, msg.as_string())
    sender.quit()

def get_mimetypes(path):
    m = magic.from_file(path, mime=True).split('/')
    types = dict(maintype = m[0], subtype = m[1])
    return types


