from flask import Flask, jsonify
from flask import render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from .common import execute_query

import os
import sqlite3

from .common import db_location

app = Flask(__name__)

app.config['SECRET_KEY'] = "rols123"
app.config['UPLOAD_FOLDER'] = "/root/pyserver/"
app.config['MAX_CONTENT_PATH'] = 10000000

@app.route("/")  # this sets the route to this page
def home():

        return jsonify({'Message': "Working"})

@app.route("/upload")
def upload_bot():
	return render_template('upload.html')

def add_file_to_base(botname, passw):
	with sqlite3.connect(db_location) as conn:
		cur = conn.cursor()
		cur.execute(
			"insert into uploadedfiles(bot, userpass) values (?,?)",
			(botname, passw))
		conn.commit()


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      botname = request.form["botname"]
      passw = request.form["pass"]
      botname = "bot_" + passw + "_" + botname
      #os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], botname), exist_ok=True)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], botname + ".py"))

      add_file_to_base(botname, passw)

      return f'file uploaded successfully, under passwd {request.form["pass"]}'

@app.route('/games')
def list_games():
      res = execute_query("select * from runs")
      headers = ["player1", "player2", "map", "time added", "time played", "finished", "score1", "score2"]

      res = sorted(res, key=lambda x: x[4], reverse=True)
      return render_template(
        'games.html',
        headers=headers,
        tableData=res
    )


@app.route('/rank')
def rank():
      res = execute_query("select * from rankings")
      headers = ["player1", "wins", "loses", "score", "rank"]

      res = sorted(res, key=lambda x: x[4], reverse=True)

      return render_template(
        'rankings.html',
        headers=headers,
        tableData=res
    )


if __name__ == "__main__":

    app.run(debug=True)
