from flask import Blueprint, request, g, Response, Flask
import json

from .database import get_db

from . import socials
from . import events
from . import assos
from . import sessions


# api blueprint and helpers

api = Blueprint('api', __name__)

def success(data, status=200):
    return json.dumps({'success': True, 'data': data}, default=str), status, {'ContentType': 'application/json'}

def error(message, status=400):
    return json.dumps({'success': False, 'error': message}, default=str), status, {'ContentType': 'application/json'}

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


# ics

from ics import Calendar, Event
from ics.grammar.parse import ContentLine

def add_events_to_calendar(cal, events):
    for event in events:
        asso_name = event['asso'].split(',')[0]
        e = Event()
        e.uid = str(event['id'])
        e.name = '[' + asso_name + '] ' + event['title']
        e.begin = event['date']
        e.location = event['place']
        if event['duration']:
            e.duration = {'minutes': event['duration']}
        e.organizer = asso_name
        e.last_modified = event['lastUpdateDate']
        e.created = event['createDate']
        e.url = event['link']
        #e.status = event['status']
        e.description = event['description']
        e.extra.append(ContentLine('COLOR', {}, event['color']))
        if event['poster']:
            e.extra.append(ContentLine('IMAGE', {}, event['poster']))
        cal.events.add(e)

@api.route('/events.ics', methods=['GET'])
def get_events_ics():
    # get events
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id")
    events = mycursor.fetchall()
    # create ics calendar
    cal = Calendar()
    name = 'Tous les événements - Tekiens.net'
    cal.extra.append(ContentLine('X-WR-CALNAME', {}, name))
    cal.extra.append(ContentLine('NAME', {}, name))
    add_events_to_calendar(cal, events)
    return Response(cal.serialize(), mimetype='text/calendar')

@api.route('/assos/<id>/events.ics', methods=['GET'])
def get_asso_events_ics(id):
    # get events and asso
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM assos WHERE id = %s", (id,))
    asso = assos.parse_asso(mycursor.fetchone())
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id WHERE asso_id = %s", (id,))
    events = mycursor.fetchall()
    # create ics calendar
    cal = Calendar()
    name = asso['names'][0] + ' - Tekiens.net'
    cal.extra.append(ContentLine('X-WR-CALNAME', {}, name))
    cal.extra.append(ContentLine('NAME', {}, name))
    cal.extra.append(ContentLine('COLOR', {}, asso['color']))
    add_events_to_calendar(cal, events)
    return Response(cal.serialize(), mimetype='text/calendar')



# email templating

from . import mail
api.register_blueprint(mail.blueprint, url_prefix='/mail')

# socials

api.register_blueprint(socials.blueprint, url_prefix='/socials')