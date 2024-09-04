from flask import Blueprint, g
import secrets
from hashlib import sha256

from .. import api
from ..database import get_db


blueprint = Blueprint('sessions', __name__)

@blueprint.route('/<id>', methods=['GET'])
def get_sessions(id):
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM sessions WHERE id = %s", (id,))
    session = mycursor.fetchone()
    if not session:
        return api.error('Not found', 404)
    return api.success(session)

@blueprint.route('', methods=['POST'])
def post_session():
    asso_id = g.args.get('asso')
    hash_client = g.args.get('hash') # get the hash from the client if it exists

    if not asso_id:
        return api.error('Missing parameters')

    mydb = get_db() # connect to the database
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT password, challenge, id FROM assos WHERE id = %s", (asso_id,))
    asso = mycursor.fetchone()

    if not asso:
        return api.error('Invalid asso', 400)

    if not hash_client:
        #generate  the challenge and hash it with the password to send it to the client
        challenge = secrets.token_urlsafe(24)
        password = asso['password'].split('$')

        salt= '$'+password[1]+'$'+password[2]+'$'+password[3][:22]
        print(salt)
        mycursor.execute("UPDATE assos SET challenge = %s WHERE id = %s", (challenge, asso_id))

        return api.success({'challenge' : challenge,'salt' : salt}, 201)

    #check if the challenge exist and if the client send the hash of the challenge
    if hash_client and asso['challenge']:

        #hash the challenge with the password and compare it with the hash send by the client
        hash_serv = sha256((asso['challenge']+ asso['password']).encode()).hexdigest()


        if hash_client==hash_serv:
            #if the hash are the same, create a session and return the id of the session (and delete the challenge in the database)
            session_id = secrets.token_urlsafe(24)
            mycursor.execute("INSERT INTO sessions (id, asso_id) VALUES (%s, %s)", (session_id, asso['id']))
            mycursor.execute("UPDATE assos SET challenge = NULL WHERE id = %s", (asso_id,))
            return api.success({'id': session_id, 'asso_id': asso['id']}, 201)

    return api.error('Invalid credentials', 401)

@blueprint.route('/<id>', methods=['DELETE'])
def delete_session(id):
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("DELETE FROM sessions WHERE id = %s", (id,))
    return api.success(None)