from flask import Flask, jsonify
from flask import render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import os
import sqlite3

from common import db_location

app = Flask(__name__)

app.config['SECRET_KEY'] = "rols123"
app.config['UPLOAD_FOLDER'] = "/root/pyserver/bots/"
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
      botname = passw + "_" + botname
      os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], botname), exist_ok=True)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], botname, botname + ".py"))

      add_file_to_base(botname, passw)

      return f'file uploaded successfully, under passwd {request.form["pass"]}'


if __name__ == "__main__":

    app.run(debug=True)
