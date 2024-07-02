
from flask import Blueprint, request, g

from .database import get_db
from . import mail
from . import api
from . import events
from . import assos


# Create blueprint for templates API

blueprint = Blueprint('mail', __name__)

@blueprint.route('', methods=['GET'])
def get_templates():
    return api.success(mail.get_templates())

@blueprint.route('/<id>', methods=['GET'])
def get_template(id):

    template = mail.get_template(id)
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

    return api.success(mail.render(template, {
        'event': event,
        'asso': asso,
        'site': request.scheme + '://' + request.host + request.root_path
    }))