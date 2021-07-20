from flask import Flask, jsonify

import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'InsuranceDB'
DB_USER = 'postgres'
DB_PASS = 'Tcs#1234'

conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = '5432')
    


# Customers = db.Table('customer', db.metadata, autoload = True, autoload_with = db.engine)


@app.route('/')
def claimS():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    s = '''SELECt * from msaccess.customer'''
    #''' in this string syntax you can pass anything as it is compared to other where you have to escape ; or write new line as \n here enter is passed as new newlinw
    cur.execute(s)
    list_claims = cur.fetchall()
    print(list_claims)



if __name__ == '__main__':
    app.run(debug=True)

