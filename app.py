# complete imports
from flask import Flask, request, Response, jsonify
import json
import os
import dj_database_url
from flask_sqlalchemy import SQLAlchemy
import psycopg2


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://take_home_exam_postgres_user:fu1pGB2ozwor7weJ1C09G3kSZ5vvLoVp@dpg-covu3m021fec73frjie0-a.oregon-postgres.render.com/take_home_exam_postgres"
DATABASE_URL = "postgresql://take_home_exam_postgres_user:fu1pGB2ozwor7weJ1C09G3kSZ5vvLoVp@dpg-covu3m021fec73frjie0-a.oregon-postgres.render.com/take_home_exam_postgres"


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
# cur.execute("DROP TABLE history")
cur.execute("""CREATE TABLE history(
        operator VARCHAR(1),
        num1 INTEGER,
        num2 INTEGER,
        result INTEGER);
        """)
conn.commit()
cur.close()
conn.close()

# single route '/message' accepting GET method
@app.route("/message", methods = ["GET"])
def handleInput():
    # pull data from request body
    requestJSON = request.get_json()
    requestMessage = requestJSON["data"]["message"]
    # strip whitespace
    requestMessage = requestMessage.strip()

    # if message starts with "/"
    if requestMessage[0] == "/":
        # split into two parts based on first whitespace following "/"
        splitCommand = requestMessage.split(' ', 1)
        # assign first part less the "/" to the command variable
        command = splitCommand[0][1:]
        # assign the rest to the message variable
        message = splitCommand[1]
        if command == 'add':
            return add(message)
        elif command == 'sub':
            return sub(message)
        elif command == 'history':
            return history()
    # if message does not start with "/"
    else:
        command = None
        message = requestMessage
        return jsonify({
           "data": {"command": command, "message": message }
        })




@app.route("/add", methods = ["GET"])
def add():
    requestJSON = request.get_json()
    requestMessage = requestJSON["data"]["message"]
    # strip whitespace
    requestMessage = requestMessage.strip()
    splitMessage = requestMessage.split(' ', 1)
    try:
        float1 = splitMessage[0]
        float2 = splitMessage[1]
        float1 = int(float1)
        float2 = int(float2)
        result = float1 + float2
    except:
        return jsonify({
           "data": {"message": "Invalid input to command" }
        })
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO history(operator, num1, num2, result) VALUES('+', " + str(float1) + ", " + str(float2) + ", " + str(result) + ")")

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
           "data": {"message": str(float1 + float2) }
        })

@app.route("/sub", methods = ["GET"])
def sub():
    requestJSON = request.get_json()
    requestMessage = requestJSON["data"]["message"]
    # strip whitespace
    requestMessage = requestMessage.strip()
    splitMessage = requestMessage.split(' ', 1)
    try:
        float1 = splitMessage[0]
        float2 = splitMessage[1]
        float1 = int(float1)
        float2 = int(float2)
        result = float1 - float2
    except:
        return jsonify({
           "data": {"message": "Invalid input to command" }
        })
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO history(operator, num1, num2, result) VALUES('-', " + str(float1) + ", " + str(float2) + ", " + str(result) + ")")

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
           "data": {"message": str(float1 - float2) }
        })

@app.route("/history", methods = ["GET"])
def history():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM history;')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    build = ""
    for row in rows:
        build += str(row[1]) + str(row[0]) + str(row[2]) + '=' + str(row[3])
        build += " "
    return jsonify({
           "data": {"message": build }
        })