from flask import Blueprint, g

from .. import api
from ..database import get_db
from . import data


# only use editable columns
events_columns = ['title', 'poster', 'description', 'date', 'place', 'duration', 'price', 'link', 'access', 'status', 'capacity']
events_needed_columns = ['title', 'date', 'place']

# convert event from database format to API response format
def parse_event(event):
    event['poster'] = '/' + data.get_event_poster_path(event['asso_id'], event['title'], event['date']) if event['poster'] else None
    return event

# convert event from API query format to database format
def unparse_event(event):
    if 'poster' in event:
        event['poster'] = bool(event['poster'])
    return event


# create routes for events API
blueprint = Blueprint('events', __name__)

@blueprint.route('', methods=['GET'])
def get_events():
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT events.* FROM events JOIN assos ON assos.id = events.asso_id WHERE 1=1"
    params = ()
    if 'before' in g.args:
        sql += " AND date < %s"
        params += (g.args.get('before'),)
    if 'after' in g.args:
        sql += " AND DATE_ADD(date, INTERVAL IFNULL(duration, 0) MINUTE) > %s"
        params += (g.args.get('after'),)
    if 'campus' in g.args and type(g.args.get('campus')) is list:
        sql += " AND campus IN (''" + (", %s" * len(g.args.get('campus'))) + ")"
        params += tuple(g.args.get('campus'))
    if 'order' in g.args and g.args.get('order') == 'random':
        sql += " ORDER BY " + "RAND()"
    else:
        sql += " ORDER BY date"
    if 'desc' in g.args:
        sql += " DESC"
    sql_for_count = sql.replace("events.*", "COUNT(*) as count", 1)
    params_for_count = params
    if 'limit' in g.args and int(g.args.get('limit')) >= 0:
        sql += " LIMIT %s"
        params += (int(g.args.get('limit')),)
    if 'offset' in g.args and int(g.args.get('offset')) > 0:
        sql += " OFFSET %s"
        params += (int(g.args.get('offset')),)
    mycursor.execute(sql, params)
    events = [parse_event(event) for event in mycursor.fetchall()]
    # Second SQL query to get count
    mycursor.execute(sql_for_count, params_for_count)
    count = mycursor.fetchone()['count']
    return api.success(events, count=count)

@blueprint.route('', methods=['POST'])
def post_event():
    session_id = g.args.get('session')
    if not session_id:
        return api.error('Missing session')
    new_event = unparse_event({k: v for k, v in g.args.items() if k in events_columns})
    if not all([k in new_event for k in events_needed_columns]):
        return api.error('Missing parameters')
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    session = mycursor.fetchone()
    if not session:
        return api.error('Unauthorized', 403)
    mycursor.execute("INSERT INTO events (asso_id" + ''.join([f', {k}' for k in new_event.keys()]) + ") VALUES (%s" + (', %s' * len(new_event)) + ");", (session['asso_id'], *new_event.values()))
    if g.args.get('poster'):
        data.create_event_poster(session['asso_id'], new_event['title'], new_event['date'], g.args.get('poster'))
    return api.success({'id': mycursor.lastrowid})

@blueprint.route('/<id>', methods=['GET'])
def get_event(id):
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    result = mycursor.fetchone()
    if not result:
        return api.error('Not found', 404)
    event = parse_event(result)
    return api.success(event)

@blueprint.route('/<id>', methods=['PUT', 'PATCH'])
def put_event(id):
    session_id = g.args.get('session')
    if not session_id:
        return api.error('Missing session')
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT *, (asso_id = (SELECT asso_id FROM sessions WHERE id = %s)) AS editable FROM events WHERE id = %s", (session_id, id,))
    event = mycursor.fetchone()
    if not event:
        return api.error('Not found', 404)
    if not event['editable']:
        return api.error('Unauthorized', 403)
    new_event = unparse_event({k: v for k, v in g.args.items() if k in events_columns})
    if len(new_event) == 0:
        return api.error('Nothing to update', 200)
    sql = "UPDATE events SET " + ', '.join([f"{k} = %s" for k in new_event.keys()]) + " WHERE id = %s"
    mycursor.execute(sql, (*new_event.values(), id))
    poster_path = data.update_event_poster(event['asso_id'], event['title'], event['date'], title=new_event.get('title'), date=new_event.get('date'))
    if 'poster' in g.args:
        if g.args['poster']:
            data.create_image(poster_path, g.args.get('poster'))
        else:
            data.delete_event_poster(event['asso_id'], event['title'], event['date'])
    return api.success('Updated')

@blueprint.route('/<id>', methods=['DELETE'])
def delete_event(id):
    session = g.args.get('session')
    if not session:
        return api.error('Missing session')
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT *, (asso_id = (SELECT asso_id FROM sessions WHERE id = %s)) AS editable FROM events WHERE id = %s", (session, id,))
    event = mycursor.fetchone()
    if not event:
        return api.error('Not found', 404)
    if not event['editable']:
        return api.error('Unauthorized', 403)
    mycursor.execute("DELETE FROM events WHERE id = %s", (id,))
    data.delete_event_poster(event['asso_id'], event['title'], event['date'])
    return api.success(None)