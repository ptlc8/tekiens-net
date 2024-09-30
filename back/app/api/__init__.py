from flask import Blueprint, request, g
import json

from . import assos
from . import emails
from . import events
from . import sessions
from . import templates
from . import socials


# api blueprint and helpers

api = Blueprint('api', __name__)

def success(data, status=200, **kwargs):
    return json.dumps({'success': True, 'data': data, **kwargs}, default=str), status, {'ContentType': 'application/json'}

def error(message, status=400, **kwargs):
    return json.dumps({'success': False, 'error': message, **kwargs}, default=str), status, {'ContentType': 'application/json'}


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
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, HEAD, PUT, PATCH, DELETE"
    return response


# assos
api.register_blueprint(assos.blueprint, url_prefix='/assos')


# events
api.register_blueprint(events.blueprint, url_prefix='/events')


# sessions
api.register_blueprint(sessions.blueprint, url_prefix='/sessions')


# email templating
api.register_blueprint(templates.blueprint, url_prefix='/templates')


# socials
api.register_blueprint(socials.blueprint, url_prefix='/socials')

# emails
api.register_blueprint(emails.blueprint, url_prefix='/emails')