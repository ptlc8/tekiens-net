import os
import chevron
import markdown
from flask import Blueprint, request, g

from .database import get_db
from . import api
from . import events
from . import assos


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


# Create blueprint for mail API

blueprint = Blueprint('mail', __name__)

@blueprint.route('/templates', methods=['GET'])
def get_templates():
    return api.success(get_templates())

@blueprint.route('/templates/<id>', methods=['GET'])
def get_template(id):

    template = get_template(id)
    if template is None:
        return api.error('Not found', 404)

    event_id = g.args.get('event')
    if not event_id:
        return api.success(template)

    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    result = mycursor.fetchone()
    if not result:
        return api.error('Not found', 404)
    event = events.parse_event(result)

    mycursor.execute("SELECT * FROM assos WHERE id = %s", (event['asso_id'],))
    result = mycursor.fetchone()
    asso = assos.parse_asso(result)

    return api.success(render(template, {
        'event': event,
        'asso': asso,
        'site': request.scheme + '://' + request.host + request.root_path
    }))