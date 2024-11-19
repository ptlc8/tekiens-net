from ics import Calendar, Event
from ics.grammar.parse import ContentLine

from flask import Response, request

from .database import get_db
from .api.events import parse_event
from .api.assos import parse_asso

def create_event(event, base_url):
    e = Event()
    e.uid = str(event['id'])
    asso_name = event['asso'].split(',')[0]
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
        e.extra.append(ContentLine('IMAGE', {}, base_url + event['poster']))
    return e

def create_ics(name, events, base_url="", color=None):
    cal = Calendar()
    cal.extra.append(ContentLine('X-WR-CALNAME', {}, name))
    cal.extra.append(ContentLine('NAME', {}, name))
    if color:
        cal.extra.append(ContentLine('COLOR', {}, color))
    for event in events:
        event = parse_event(event)
        e = create_event(event, base_url)
        cal.events.add(e)
    return cal.serialize()


def get_events():
    # get events
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id")
    events = mycursor.fetchall()
    # create ics calendar
    name = 'Tous les événements - Tekiens.net'
    cal = create_ics(name, events, base_url = request.url_root)
    return Response(cal, mimetype='text/calendar')

def get_event(id):
    # get events
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id where events.id = %s", (id,))
    event = mycursor.fetchone()
    # create ics calendar
    name = event
    cal = create_ics(name, [event], base_url = request.url_root)
    return Response(cal, mimetype='text/calendar')

def get_asso_events(id):
    # get events and asso
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM assos WHERE id = %s", (id,))
    asso = parse_asso(mycursor.fetchone())
    mycursor.execute("SELECT events.*, assos.names AS asso, assos.color FROM events JOIN assos ON events.asso_id = assos.id WHERE asso_id = %s", (id,))
    events = mycursor.fetchall()
    # create ics calendar
    name = asso['names'][0] + ' - Tekiens.net'
    cal = create_ics(name, events, color=asso['color'], base_url=request.url_root)
    return Response(cal, mimetype='text/calendar')
