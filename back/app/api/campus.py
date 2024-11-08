from flask import Blueprint

from ..database import get_db
from .. import api

blueprint = Blueprint('campus', __name__)

@blueprint.route('/', methods=['GET'])
def get_campus():
    mydb = get_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT name FROM campus", ())
    campuses = mycursor.fetchall()
    return api.success(campuses)