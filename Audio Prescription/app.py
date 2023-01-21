from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from flask_mysqldb import MySQL
import mysql
from datetime import date
from codec_change_opus_to_pcm import *
from pcmtotext import *
import speech_recognition as sr
import datetime
from werkzeug.utils import secure_filename

r = sr.Recognizer()

app = Flask(__name__)

app.secret_key = 'your_secret_key'

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
    emailID=request.args.get("email")
    result="TBD"
    DOP=date.today()

    values=[name, emailID, DOP, result]
    query="INSERT INTO audioprescription(Name,emailID,DOP,result) VALUES(%s,%s,%s,%s)"
    executeQuery(query,values)
    return "I"

@app.route('/audioRecog', methods=['GET','POST'])
def audioRecog():
    print("audioRecog")
    audioFile=request.files.get("myAudio")
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sample_input_{time_stamp}_{secure_filename(audioFile.filename)}"
    
    path=f'audio/input_audio/{filename}'
    audioFile.save(path)
    # filePath(path)
    
    print('Please wait while the audio gets transcribed. This process may take up to a minute.')
    output=codecChange(path)
    session['output']=output
    return redirect(url_for('speechToTextTransform'))

@app.route('/speechToTextTransform', methods=['GET','POST'])
def speechToTextTransform():
    output = session.get('output')
    print(type(output))
    print("output ie filename is:",output)
    text = speechToText(output)
    return render_template("symptoms.html",name=text)

if __name__ == '__main__':
    app.run(debug=True)