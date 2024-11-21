from smtplib import SMTP, SMTP_SSL
from email.message import EmailMessage
import ssl
import os
import chevron
import markdown

# Setup SMTP connection
smtp_address = os.environ.get("SMTP_ADDRESS")
smtp_port = os.environ.get("SMTP_PORT")
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")
is_smtp_supported = smtp_address and smtp_port
if not is_smtp_supported:
    print("Warning: not all required smtp related environment variables are set")

smtp_server = None
if is_smtp_supported:
    try:
        if os.environ.get("SMTP_TLS") != "false": # Default to true
            server = SMTP_SSL(smtp_address, smtp_port, context=ssl.create_default_context())
        else:
            server = SMTP(smtp_address, smtp_port)
        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)
        smtp_server = server
    except Exception as e:
        is_smtp_supported = False
        print(e)

def send_email(to, subject, body):
    message = EmailMessage()
    message["From"] = smtp_address
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body, subtype="html")
    smtp_server.send_message(message)

def get_templates():
    return [filename.rsplit(".", 1)[0] for filename in os.listdir("templates") if filename.endswith(".mustache")]

def get_template(template_id):
    path = os.path.join("templates", f"{template_id}.mustache")
    if not os.path.exists(path):
        return None
    return open(path).read()

def render(template, data):
    if data["event"]["description"]:
        data["event"]["description"] = markdown.markdown(data["event"]["description"], extensions=['tables'])
    return chevron.render(template, data)