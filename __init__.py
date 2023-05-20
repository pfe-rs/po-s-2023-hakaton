import os
from flask import Flask, jsonify
from flask import render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from .common import execute_query

rel_path = os.path.dirname(os.path.realpath(__file__))
image_loc = os.path.join(rel_path, "renders")

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
      if len(botname) == 0 or len(passw) == 0:
         return "FAILED: botname and passw have to be non empty"
      if not botname.replace('_', '').isalnum() or not passw.replace('_', '').isalnum():
         return "FAILED: botname and passw can contain only _ and alfanum"
      if len(botname) > 50 or len(passw) > 50:
         return "FAILED: botname and passw have to be shorter than 50"
      botname = "bot_" + passw + "_" + botname
      #os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], botname), exist_ok=True)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], botname + ".py"))

      add_file_to_base(botname, passw)

      return f'file uploaded successfully, under passwd {request.form["pass"]}'

@app.route('/games')
def list_games():
      res = execute_query("select * from runs")
      headers = ["player1", "player2", "map", "time added", "time played", "finished", "score1", "score2", "link"]

      res = [list(single_res) for single_res in res]

      for single_res in res:
            single_res.append(f"/render/{single_res[0]}/{single_res[1]}/{single_res[2]}/0")

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

@app.route('/render/<bot1>/<bot2>/<map>/<turn>')
def renderimg(bot1, bot2, map, turn):
      next_turn = (int(turn) + 1) % 128
      prev_turn = (int(turn) + 127) % 128
      
      return render_template(
            "render.html",
            first_turn = turn,
            img_pref = f"/static/{bot1}_{bot2}_{map}_"
      )
      

if __name__ == "__main__":

    app.run(debug=True)
