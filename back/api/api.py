from flask import Blueprint, request, g, Response, Flask
import json

from .database import get_db

from . import assos
from . import events
from . import sessions
from . import ics
from . import templates
from . import socials


# api blueprint and helpers

api = Blueprint('api', __name__)

def success(data, status=200):
    return json.dumps({'success': True, 'data': data}, default=str), status, {'ContentType': 'application/json'}

def error(message, status=400):
    return json.dumps({'success': False, 'error': message}, default=str), status, {'ContentType': 'application/json'}


# parse all args from url and form
@api.url_value_preprocessor
def url_value_preprocess(endpoint, values):
    g.args = {}
    for k in request.args.keys():
        if k.endswith('[]'):
            g.args[k[0:-2]] = request.args.getlist(k) or None
        else:
            g.args[k] = request.args.get(k) or None
    for k in request.form.keys():
        if k.endswith('[]'):
            g.args[k[0:-2]] = request.form.getlist(k) or None
        else:
            g.args[k] = request.form.get(k) or None


# CORS
@api.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


# assos
api.register_blueprint(assos.blueprint, url_prefix='/assos')


# events
api.register_blueprint(events.blueprint, url_prefix='/events')


# sessions
api.register_blueprint(sessions.blueprint, url_prefix='/sessions')


# all events ics
@api.route('/events.ics', methods=['GET'])
def get_events_ics():
    # get events
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id")
    events = mycursor.fetchall()
    # create ics calendar
    name = 'Tous les événements - Tekiens.net'
    cal = ics.create_ics(name, events)
    return Response(cal, mimetype='text/calendar')


# email templating
api.register_blueprint(templates.blueprint, url_prefix='/templates')


# socials
api.register_blueprint(socials.blueprint, url_prefix='/socials')