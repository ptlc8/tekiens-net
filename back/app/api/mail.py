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
smtp_tls = os.environ.get("SMTP_TLS") == "true" if os.environ.get("SMTP_TLS") else smtp_port == "465"
smtp_from = os.environ.get("SMTP_FROM") or smtp_address

is_smtp_supported = smtp_address and smtp_port
if not is_smtp_supported:
    print("Warning: not all required smtp related environment variables are set")

smtp_server = None
if is_smtp_supported:
    try:
        if smtp_tls:
            server = SMTP_SSL(smtp_address, smtp_port, context=ssl.create_default_context())
        else:
            server = SMTP(smtp_address, smtp_port)
        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)
        smtp_server = server
        is_smtp_supported = server.noop()[0] == 250
    except Exception as e:
        is_smtp_supported = False
        if hasattr(e, "message"):
            print(f"Warning: SMTP: {e.message}")
        print(f"Warning: SMTP: {e}")
    finally:
        print(f"Info: SMTP server is {'up' if is_smtp_supported else 'down'}")

def send_email(to, subject, body, from_name=None):
    message = EmailMessage()
    message["From"] = from_name + ' <' + smtp_from + '>' if from_name else smtp_from
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