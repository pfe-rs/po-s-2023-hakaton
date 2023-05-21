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


@app.route('/games_no_score')
def list_games_no_score():
      res = execute_query("select * from runs")
      headers = ["player1", "player2", "map", "time added", "time played", "finished", "link"]

      res = [r[:6] for r in res]

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

      player1 = bot1.split("_")[1]
      player2 = bot2.split("_")[1]
      name1 = "_".join(bot1.split("_")[2:])
      name2 = "_".join(bot2.split("_")[2:])
      img_prefix = f"/static/{bot1}_{bot2}_{map}_"
      
      return render_template(
            "render.html",
            first_turn = turn,
            img_pref = img_prefix,
            player1=player1,
            player2=player2,
            name1=name1,
            name2=name2
      )
      

def calc_res(matches):
     
     for mch in match

@app.route('/ranktour')
def rank():
      res = execute_query("select * from runs where run = 'true'")
      
      bot_res = {}
      bots = set()
      for r in res:
            bot1, bot2 = r[0], r[1]
            if bot2 < bot1:
                  bot1, bot2 = bot2, bot1
            k = (bot1, bot2)
            if k not in bot_res:
                  bot_res[k] = []
            bot_res[k].append(r)
            bots.add(bot1)
            bots.add(bot2)

      bots = list(bots)

      bot_score = {}
      for k, r_list in bot_res.items():
            score = 0
            for r in r_list:
                  if r[6] > r[7]:
                        score += 1
                  if r[6] < r[7]:
                        score -= 1
            bot_score[k] = score
      
      


      res = sorted(res, key=lambda x: x[4], reverse=True)

      return render_template(
        'rankings.html',
        headers=headers,
        tableData=res
    )

if __name__ == "__main__":

    app.run(debug=True)
