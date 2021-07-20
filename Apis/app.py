from datetime import date
from os import stat
from flask import Flask, jsonify, request

import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'InsuranceDB'
DB_USER = 'postgres'
DB_PASS = 'Tcs#1234'

conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = '5432')
    


@app.route('/customerClaimDetails')
def claimS():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    s = '''select * from msaccess.claim full outer join msaccess.claim_file on msaccess.claim.claim_id = msaccess.claim_file.claim_id full outer join msaccess.damage_in_claim on msaccess.claim.claim_id = msaccess.damage_in_claim.claim_id; '''
    #''' in this string syntax you can pass anything as it is compared to other where you have to escape ; or write new line as \n here enter is passed as new newlinw
    cur.execute(s)
    list_claims = cur.fetchall()
    maintemp = []
    for row in list_claims:
        temp = []
        for l in row:
            l = str(l)
            temp.append(l)
        maintemp.append(temp)
    # print(list_claims)
    return jsonify(maintemp)


@app.route('/customerPolicyDetails')
def getPolicyDetails():
    print('okay')
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    s = '''SELECt * from msaccess.customer'''
    #''' in this string syntax you can pass anything as it is compared to other where you have to escape ; or write new line as \n here enter is passed as new newlinw
    cur.execute(s)
    list_claims = cur.fetchall()
    return jsonify(list_claims)



@app.route('/customerAuthDetails/<string:username>')
def authDetails(username):
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    s = '''SELECt * from msaccess.customer'''
    cur.execute(s)
    authdetails = cur.fetchall()
    dict = {}
    for row in authdetails:
        dict[row[0]] = row[-1]
    if username not in dict:
        return 'User Not found'
    else:
        temp = dict[str(username)]
        return temp


@app.route('/customerClaimDatails', methods = ['POST'])
def postClaimDetails():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if request.method == 'POST':
        claimdetails = request.get_json(force=True)
        claim_id = int(claimdetails['claim_id'])
        policy_id = str(claimdetails['policy_id'])
        claim_descr = str(claimdetails['claim_descr'])
        date_requested = (claimdetails['date_requested'])
        date_requested = str(date_requested)
        print(type(date_requested))
        user_id = str(claimdetails['user_id'])
        total_amount = float(claimdetails['total_amount'])
        status = str(claimdetails['status'])
        cur.execute("INSERT INTO msaccess.claim(claim_id, policy_id, claim_descr, date_requested, user_id, total_amount, status) VALUES (%s,%s,%s,%s,%s,%s,%s)", (claim_id, policy_id, claim_descr, date_requested,user_id, total_amount,status))
        conn.commit()
        return "Data Inserted Successfully"


@app.route('/claimAnnotatedImage', methods = ['POST'])
def postClaimFile():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if request.method == 'POST':
        claimdetails = request.get_json(force=True)
        claim_file_id = int(claimdetails['claim_file_id'])
        claim_id = int(claimdetails['claim_id'])
        agent_id = str(claimdetails['agent_id'])
        policy_id = str(claimdetails['policy_id'])
        date_uploaded = (claimdetails['date_uploaded'])
        date_uploaded = str(date_uploaded)
        file_location = str(claimdetails['file_location'])
        claim_notes = str(claimdetails['claim_notes'])
        image = str(claimdetails['image'])
        video = str(claimdetails['video'])
        cur.execute("INSERT INTO msaccess.claim_file(claim_file_id, claim_id, agent_id, policy_id, date_uploaded, file_location, claim_notes, image, video) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (claim_file_id, claim_id, agent_id, policy_id, date_uploaded, file_location, claim_notes, image, video))
        conn.commit()
        return "Data Inserted Successfully"


@app.route('/claimEstimatesFromMLModel', methods = ['POST'])
def postClaimEstimates():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if request.method == 'POST':
        claimdetails = request.get_json(force=True)
        part_id = str(claimdetails['part_id'])
        claim_id = int(claimdetails['claim_id'])
        damage_type = str(claimdetails['damage_type'])
        quantity = int(claimdetails['quantity'])
        cost = float(claimdetails['cost'])
        status = str(claimdetails['status'])
        cur.execute("INSERT INTO msaccess.damage_in_claim(part_id, claim_id, damage_type, quantity, cost, status) VALUES (%s,%s,%s,%s,%s,%s)", (part_id, claim_id, damage_type, quantity, cost,status))
        conn.commit()
        return "Data Inserted Successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

