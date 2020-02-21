import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import ssl
import mimetypes

import info

def create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg

def attach_file(msg, file_list):
    for f in file_list:
        with open(f, 'rb') as fp:
            types = get_mimetypes(f)
            attachment = MIMEBase(types['maintype'], types['subtype'])
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition', 'attachment',
                filename = f
            )
            msg.attach(attachment)

def add_text(msg, body):
    msg.attach(MIMEText(body))

def send_mail(from_addr, to_addrs, password, msg):
    sender = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    sender.login(from_addr, password)
    sender.sendmail(from_addr, to_addrs, msg.as_string())
    sender.quit()

def get_mimetypes(f):
    m = mimetypes.guess_type(f)[0].split('/')
    types = dict(maintype = m[0], subtype = m[1])
    return types

if __name__ == '__main__':
    from_addr = info.FROM_ADDRESS
    to_addr = info.TO_ADDRESS
    cc_addrs = info.CC
    bcc_addrs = info.BCC
    subject = info.SUBJECT
    body = info.BODY
    password = info.PASSWORD
    file_list = info.FILE_LIST

    msg = create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject)
    add_text(msg, body)
    attach_file(msg, file_list)
    send_mail(from_addr, to_addr, password, msg)

