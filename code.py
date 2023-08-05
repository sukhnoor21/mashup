import os
import re
import smtplib
import webbrowser
import urllib.request
from waitress import serve
from pytube import YouTube
from email import encoders
from zipfile import ZipFile
from pydub import AudioSegment
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from flask import Flask, request
app=Flask(__name__) 
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        f=AudioSegment.empty()
        for i in range(int(request.form['number_of_videos'])):
            f+=AudioSegment.from_file(YouTube('https://www.youtube.com/watch?v='+re.findall(r'watch\?v=(\S{11})',urllib.request.urlopen('https://www.youtube.com/results?search_query='+str(request.form['singer_name'].replace(' ', '+'))).read().decode())[i]).streams.filter(only_audio=True).first().download(filename=str(i)))[:int(request.form['audio_duration'])* 1000]
            os.remove(str(i))
        f.export('mashup')
        with ZipFile('mashup.zip','w') as zip:
            zip.write('mashup')
        os.remove('mashup')
        m=MIMEMultipart()
        with open('mashup.zip',"rb") as attachment:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",f"attachment;filename={'mashup.zip'}",)
        m.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login('mashupwebservice@gmail.com','vohhegrtknjctdyp')
            server.sendmail('mashupwebservice@gmail.com',request.form['email'],m.as_string())
        os.remove('mashup.zip')
    return '''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>Mashup Web Service</title>
        <style>
          body {
            background-color: lightgray;
          }
          form {
            padding: 20px;
            width: 35%;
            margin: 20px auto;
            text-align: center;
            border: 1px solid lightgray;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0px 0px 10px gray;
          }
          h1 {
            text-align: center;
            margin: 20px 0;
            color: black;
            text-shadow: 2px 2px 2px white;
          }
          input[type="text"],
          input[type="email"],
          input[type="number"] {
            padding: 10px;
            width: 95%;
            margin-bottom: 20px;
            font-size: 16px;
            border: 1px solid lightgray;
            border-radius: 5px;
          }
          input[type="submit"] {
            padding: 10px 20px;
            background-color: green;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
          }
        </style>
      </head>
      <body>
        <h1>Mashup Web Service</h1>
        <form method="post">
          <input type="text" id="singer_name" name="singer_name" placeholder="Singer Name" required>
          <br><br>
          <input type="number" id="number_of_videos" name="number_of_videos" min="11" placeholder="Number of Videos" required>
          <br><br>
          <input type="number" id="audio_duration" name="audio_duration" min="21" placeholder="Audio Duration (sec)" required>
          <br><br>
          <input type="email" id="email" name="email" placeholder="Email ID" required>
          <br><br>
          <input type="submit" value="Submit">
        </form>
      </body>
    </html>
    '''
if __name__=='__main__':
    webbrowser.open_new('http://127.0.0.1:5000')
    serve(app,host='127.0.0.1',port=5000)
