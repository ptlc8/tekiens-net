from flask import Blueprint, request
import json
import os
from dotenv import load_dotenv
import mysql.connector
import secrets

load_dotenv()


# database

mydb = mysql.connector.connect(
    host=os.environ.get('DATABASE_HOST'),
    user=os.environ.get('DATABASE_USER'),
    password=os.environ.get('DATABASE_PASS'),
    database=os.environ.get('DATABASE_NAME'),
    autocommit=True
)
mycursor = mydb.cursor(dictionary=True)

# only use editable columns
assos_columns = ['id', 'names', 'logos', 'start', 'end', 'theme', 'campus', 'room', 'socials', 'description', 'color']
events_columns = ['title', 'poster', 'description', 'date', 'place', 'price', 'link', 'access', 'status', 'capacity']
events_needed_columns = ['title', 'date', 'place']


# api blueprint and helpers

api = Blueprint('api', __name__)

def success(data, status=200):
    return json.dumps({'success': True, 'data': data}, default=str), status, {'ContentType': 'application/json'}

def error(message, status=400):
    return json.dumps({'success': False, 'error': message}, default=str), status, {'ContentType': 'application/json'}


# assos

def parse_asso(asso):
    asso['names'] = asso['names'].split(',')
    asso['logos'] = asso['logos'].split(',')
    asso['socials'] = asso['socials'].split(',')
    return asso

def unparse_asso(asso):
    if 'names' in asso:
        asso['names'] = ','.join(asso['names'])
    if 'logos' in asso:
        asso['logos'] = ','.join(asso['logos'])
    if 'socials' in asso:
        asso['socials'] = ','.join(asso['socials'])
    return asso

@api.route('/assos', methods=['GET'])
def get_assos():
    mycursor.execute("SELECT * FROM assos")
    assos = [parse_asso(asso) for asso in mycursor.fetchall()]
    return success(assos)

@api.route('/assos/<id>', methods=['GET'])
def get_asso(id):
    mycursor.execute("SELECT * FROM assos WHERE id = %s", (id,))
    result = mycursor.fetchone()
    if not result:
        return error('Not found', 404)
    asso = parse_asso(result)
    return success(asso)

@api.route('/assos/<id>', methods=['PUT', 'PATCH'])
def put_asso(id):
    session_id = request.args.get('session')
    if not session_id:
        return error('Missing session')
    mycursor.execute("SELECT * FROM sessions WHERE id = %s AND asso_id = %s", (session_id, id))
    session = mycursor.fetchone()
    if not session:
        return error('Unauthorized', 403)
    new_asso = unparse_asso({k: v for k, v in request.args.items() if k in assos_columns})
    if len(new_asso) == 0:
        return error('Nothing to update', 200)
    sql = "UPDATE assos SET " + ', '.join([f"{k} = %s" for k in new_asso.keys()]) + " WHERE id = %s"
    mycursor.execute(sql, (*new_asso.values(), id))
    return success('Updated')

@api.route('/assos/<id>/events', methods=['GET'])
def get_asso_events(id):
    mycursor.execute("SELECT * FROM events WHERE asso_id = %s ORDER BY date", (id,))
    events = mycursor.fetchall()
    return success(events)


# events

@api.route('/events', methods=['GET'])
def get_events():
    mycursor.execute("SELECT * FROM events ORDER BY date")
    events = mycursor.fetchall()
    return success(events)

@api.route('/events', methods=['POST'])
def post_event():
    session = request.args.get('session')
    if not session:
        return error('Missing session')
    new_event = {k: v for k, v in request.args.items() if k in events_columns}
    if not all([k in new_event for k in events_needed_columns]):
        return error('Missing parameters')
    mycursor.execute("INSERT INTO events (asso_id" + ''.join([f', {k}' for k in new_event.keys()]) + ") VALUES ((SELECT asso_id FROM sessions WHERE id = %s)" + (', %s' * len(new_event)) + ");", (session, *new_event.values()))
    if not mycursor.rowcount:
        return error('Unauthorized', 403)
    return success('Created')

@api.route('/events/<id>', methods=['GET'])
def get_event(id):
    mycursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = mycursor.fetchone()
    if not event:
        return error('Not found', 404)
    return success(event)

@api.route('/events/<id>', methods=['PUT', 'PATCH'])
def put_event(id):
    session_id = request.args.get('session')
    if not session_id:
        return error('Missing session')
    mycursor.execute("SELECT *, (asso_id = (SELECT asso_id FROM sessions WHERE id = %s)) AS editable FROM events WHERE id = %s", (session_id, id,))
    event = mycursor.fetchone()
    if not event:
        return error('Not found', 404)
    if not event['editable']:
        return error('Unauthorized', 403)
    new_event = {k: v for k, v in request.args.items() if k in events_columns}
    if len(new_event) == 0:
        return error('Nothing to update', 200)
    sql = "UPDATE events SET " + ', '.join([f"{k} = %s" for k in new_event.keys()]) + " WHERE id = %s"
    mycursor.execute(sql, (*new_event.values(), id))
    return success('Updated')

@api.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    session = request.args.get('session')
    if not session:
        return error('Missing session')
    mycursor.execute("SELECT *, (asso_id = (SELECT asso_id FROM sessions WHERE id = %s)) AS editable FROM events WHERE id = %s", (session, id,))
    event = mycursor.fetchone()
    if not event:
        return error('Not found', 404)
    if not event['editable']:
        return error('Unauthorized', 403)
    mycursor.execute("DELETE FROM events WHERE id = %s", (id,))
    return success('Deleted')


# sessions

@api.route('/sessions/<id>', methods=['GET'])
def get_sessions(id):
    mycursor.execute("SELECT * FROM sessions WHERE id = %s", (id,))
    session = mycursor.fetchone()
    if not session:
        return error('Not found', 404)
    return success(session)

@api.route('/sessions', methods=['POST'])
def post_session():
    asso_id = request.args.get('asso')
    password = request.args.get('password')
    if not asso_id or not password:
        return error('Missing parameters')
    # TODO: implement password
    #mycursor.execute("SELECT * FROM assos WHERE id = %s AND password = %s", (assoId, password))
    mycursor.execute("SELECT * FROM assos WHERE id = %s", (asso_id,))
    asso = mycursor.fetchone()
    if not asso:
        return error('Wrong credentials', 403)
    session_id = secrets.token_urlsafe(24)
    mycursor.execute("INSERT INTO sessions (id, asso_id) VALUES (%s, %s)", (session_id, asso['id']))
    return success({'id': session_id, 'asso_id': asso['id']}, 201)