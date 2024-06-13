#python script which take a csv file as input and change the password of the assos who is in mysql database
#the script use bcrypt to hash the password
#the csv file must have the following format: id,password

import csv
import mysql.connector
import sys
from dotenv import load_dotenv
import os
import bcrypt

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

def change_password_csv(file_name):

    try:
        mydb = get_db()
        mycursor = mydb.cursor()
        with open(file_name) as csv_file:
            #ignore the first line
            next(csv_file)
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                #hash the password
                row[1] = hash_password(row[1])
                sql = "UPDATE `assos` SET `password` = %s WHERE `id` = %s"
                val = (row[1], row[0])
                mycursor.execute(sql, val)
                mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e:
        print("An error occured: ", e)
        sys.exit(1)

def change_password(id, password):
    try:
        mydb = get_db()
        mycursor = mydb.cursor()
        #hash the password
        password = hash_password(password)
        sql = "UPDATE `assos` SET `password` = %s WHERE `id` = %s"
        val = (password, id)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e:
        print("An error occured: ", e)
        sys.exit(1)


def hash_password(password):
    try:
        #hash the password with 10 rounds
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    except Exception as e:
        print("An error occured: ", e)
        sys.exit(1)
        
if __name__ == "__main__":
    print(sys.argv, len(sys.argv))
    #if there is one argument we take it as the file name
    if len(sys.argv) == 2:
        change_password_csv(sys.argv[1])
    #if there are the parameters -p which is the password and -i which is the id
    elif len(sys.argv) == 5:
        password = sys.argv[2]
        id = sys.argv[4]
        change_password(id, password)
    else:
        print("Usage: python change_password.py <file_name> or python change_password.py -p <password> -i <id>")
        sys.exit(1)
