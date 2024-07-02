import os
import chevron
import markdown


def send_email(to, subject, body):
    print(f"Sending email to {to} with subject {subject} and body {body}")

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