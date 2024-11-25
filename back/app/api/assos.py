from flask import Blueprint, g

from .. import api
from ..database import get_db
from . import data
from .socials import parse_social
from .events import parse_event


# only use editable columns
assos_columns = ['id', 'names', 'logos', 'start', 'end', 'theme', 'campus', 'room', 'socials', 'description', 'color']

# convert asso from database format to API response format
def parse_asso(asso):
    asso['names'] = asso['names'].split(',')
    asso['logos'] = ['/' + logo for logo in data.get_asso_logos_paths(asso['id'], int(asso['logos']))]
    asso_socials = []
    for s in (asso['socials'].split(',') if asso['socials'] else []):
        asso_socials.append(parse_social(s))
    asso['socials'] = asso_socials
    asso['color'] = f'#{asso["color"]:0{6}x}'
    return asso

# convert asso from API query format to database format
def unparse_asso(asso):
    if 'names' in asso:
        asso['names'] = ','.join(asso['names'])
    if 'logos' in asso:
        asso['logos'] = len(asso['logos'])
    if 'socials' in asso:
        asso['socials'] = ','.join(asso['socials'])
    if 'color' in asso:
        try:
            asso['color'] = int(asso['color'][1:], 16)
        except ValueError:
            del asso['color']
    return asso


# create routes for assos API
blueprint = Blueprint('assos', __name__)

@blueprint.route('', methods=['GET'])
def get_assos():
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT " + ", ".join(assos_columns) + " FROM assos WHERE 1=1"
    params = ()
    if 'campus' in g.args:
        sql += " AND campus = %s"
        params += (g.args.get('campus'),)
    if 'before' in g.args:
        sql += " AND (start < %s OR start IS NULL)"
        params += (g.args.get('before'),)
    if 'after' in g.args:
        sql += " AND (end > %s OR end IS NULL)"
        params += (g.args.get('after'),)
    if 'order' in g.args and g.args.get('order') in ['start', 'end', 'color', 'random']:
        sql += " ORDER BY " + ("RAND()" if g.args.get('order') == 'random' else g.args.get('order'))
        if 'desc' in g.args:
            sql += " DESC"
    sql_for_count = sql.replace(", ".join(assos_columns), "COUNT(*) as count", 1)
    params_for_count = params
    if 'limit' in g.args and int(g.args.get('limit')) >= 0:
        sql += " LIMIT %s"
        params += (int(g.args.get('limit')),)
    if 'offset' in g.args and int(g.args.get('offset')) > 0:
        sql += " OFFSET %s"
        params += (int(g.args.get('offset')),)
    mycursor.execute(sql, params)
    assos = [parse_asso(asso) for asso in mycursor.fetchall()]
    # Second SQL query to get count
    mycursor.execute(sql_for_count, params_for_count)
    count = mycursor.fetchone()['count']
    return api.success(assos, count=count)

@blueprint.route('/<id>', methods=['GET'])
def get_asso(id):
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT " + ", ".join(assos_columns) + " FROM assos WHERE id = %s", (id,))
    result = mycursor.fetchone()
    if not result:
        return api.error('Not found', 404)
    asso = parse_asso(result)
    return api.success(asso)

@blueprint.route('/<id>', methods=['PUT', 'PATCH'])
def put_asso(id):
    session_id = g.args.get('session')
    if not session_id:
        return api.error('Missing session')
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM sessions WHERE id = %s AND asso_id = %s", (session_id, id))
    session = mycursor.fetchone()
    if not session:
        return api.error('Unauthorized', 403)
    new_asso = unparse_asso({k: v for k, v in g.args.items() if k in assos_columns})
    if len(new_asso) == 0:
        return api.error('Nothing to update', 200)
    if 'id' in new_asso and ('/' in new_asso['id'] or data.normalize(new_asso['id']) == ''):
        return api.error('Invalid id', 400)
    sql = "UPDATE assos SET " + ', '.join([f"{k} = %s" for k in new_asso.keys()]) + " WHERE id = %s"
    mycursor.execute(sql, (*new_asso.values(), id))
    if 'logos' in g.args:
        data.update_asso_logos(id, g.args.get('logos'))
    data.update_asso_folder(id, new_asso.get('id'))
    return api.success('Updated')

@blueprint.route('/<id>/events', methods=['GET'])
def get_asso_events(id):
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM events WHERE asso_id = %s"
    params = (id,)
    if 'before' in g.args:
        sql += " AND date < %s"
        params += (g.args.get('before'),)
    if 'after' in g.args:
        sql += " AND DATE_ADD(date, INTERVAL IFNULL(duration, 0) MINUTE) > %s"
        params += (g.args.get('after'),)
    if 'order' in g.args and g.args.get('order') == 'random':
        sql += " ORDER BY " + "RAND()"
    else:
        sql += " ORDER BY date"
    if 'desc' in g.args:
        sql += " DESC"
    sql_for_count = sql.replace("*", "COUNT(*) as count", 1)
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
