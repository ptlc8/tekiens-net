#!venv/bin/python
# python script which take a new asso identifier and a password as input to create a new asso in the database

import csv
import mysql.connector
import sys
from dotenv import load_dotenv
import os
from change_password import hash_password

load_dotenv()

def get_db():
    mydb = mysql.connector.connect(
        host=os.environ.get('DATABASE_HOST'),
        user=os.environ.get('DATABASE_USER'),
        password=os.environ.get('DATABASE_PASS'),
        database=os.environ.get('DATABASE_NAME'),
        autocommit=True
    )
    return mydb

def create_asso(id, password):
    try:
        mydb = get_db()
        mycursor = mydb.cursor()
        #hash the password
        password = hash_password(password)
        sql = "INSERT INTO `assos` (`id`, `names`, `password`, `logos`, `theme`, `campus`, `socials`, `color`) VALUES (%s, %s, %s, 0, '', '', '', 0)"
        mycursor.execute(sql, (id, id, password))
        mycursor.close()
        mydb.close()
    except Exception as e:
        print("An error occured: ", e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <asso_id> <password>")
        exit(1)
    else:
        create_asso(sys.argv[1], sys.argv[2])
