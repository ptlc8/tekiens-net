from flask import Blueprint, request, g

from ..database import get_db
from . import mail
from .. import api
from . import events
from . import assos


# Create blueprint for templates API

blueprint = Blueprint('templates', __name__)

@blueprint.route('', methods=['GET'])
def get_templates():
    return api.success(mail.get_templates())

@blueprint.route('/<id>', methods=['GET'])
def get_template(id):
    template = mail.get_template(id)
    if template is None:
        return api.error('Not found', 404)

    return api.success(template)

@blueprint.route('/<id>/<event_id>', methods=['GET'])
def get_email_with_template(id, event_id):
    template = mail.get_template(id)
    if template is None:
        return api.error('Not found', 404)

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

    return api.success(mail.render(template, {
        'event': event,
        'asso': asso,
        'site': request.scheme + '://' + request.host + request.root_path
    }))

@blueprint.route('/<id>/<event_id>/send', methods=['POST'])
def send_email(id, event_id):
    if not mail.is_smtp_supported:
        return api.error('Not Implemented', 501)

    session_id = g.args.get('session')
    if not session_id:
        return api.error('Missing session')

    to = g.args.get("to")
    if not to:
        return api.error('No receiver provided')

    template = mail.get_template(id)
    if template is None:
        return api.error('Not found', 404)

    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    session = mycursor.fetchone()
    if not session:
        return api.error('Unauthorized', 403)

    mycursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    result = mycursor.fetchone()
    if not result:
        return api.error('Not found', 404)
    event = events.parse_event(result)
    if event['asso_id'] != session['asso_id']:
        return api.error('Unauthorized', 403)

    mycursor.execute("SELECT * FROM assos WHERE id = %s", (event['asso_id'],))
    result = mycursor.fetchone()
    asso = assos.parse_asso(result)

    mail.send_email(to, event['title'], mail.render(template, {
        'event': event,
        'asso': asso,
        'site': request.scheme + '://' + request.host + request.root_path
    }))
    return api.success(None)
