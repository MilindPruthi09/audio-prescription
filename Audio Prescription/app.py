from flask import Flask, render_template, request
import mysql.connector
from flask_mysqldb import MySQL
import mysql
from datetime import date
from codec_change_opus_to_pcm import *
from pcmtotext import *
import speech_recognition as sr

r = sr.Recognizer()

app = Flask(__name__)

db = MySQL(app);

def executeQuery(query,values):
	conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
	cursor = conn.cursor()
	cursor.execute(query, values)
	conn.commit()
	cursor.close()

@app.route('/UI', methods=['GET','POST'])
def UI():
    return render_template("ui.html")

@app.route('/insert', methods=['GET','POST'])
def insert():
    name=request.args.get("name")
    print(name)
    emailID=request.args.get("email")
    result="TBD"
    DOP=date.today()

    values=[name, emailID, DOP, result]
    query="INSERT INTO audioPrescription(Name,emailID,DOP,result) VALUES(%s,%s,%s,%s)"
    executeQuery(query,values)
    return "I"

@app.route('/audioRecog', methods=['GET','POST'])
def audioRecog():
    print("audioRecog")
    audioFile=request.files.get("myAudio")
    path='./sample.wav'
    audioFile.save(path)
    # filePath(path)
    
    print('Please wait while the audio gets transcribed. This process may take up to a minute.')
    codecChange()
    return "I"

@app.route('/speechToTextTransform', methods=['GET','POST'])
def speechToTextTransform():
    
    text = speechToText()
    return render_template("symptoms.html",name=text)

if __name__ == '__main__':
    app.run(debug=True)