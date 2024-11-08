#import部分

import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

#定義

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)


#db作成

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_ages = db.Column(db.String(100))
    user_sex = db.Column(db.String(100))
    user_place = db.Column(db.String(100))

##アンケート部分

#page1

@app.route("/home")
def home():
    return render_template("home.html")

#page2

@app.route("/information", methods = ['GET'])
def show_form():
    with open('static/prefectures.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('information.html', prefectures=data['prefectures'])

@app.route("/useself", methods=["POST"])
def add():
    ##db追加
    #年齢
    userages = request.form.get("user_ages")
    #性別
    usersex = request.form.get("sex")
    #出身地
    userplace = request.form.get("place")

    #db格納
    user_new_data = Personal(user_ages=userages, user_sex=usersex, user_place=userplace)
    db.session.add(user_new_data)
    db.session.commit()

    # 追加したデータのIDを取得
    return redirect(url_for('show_useself', user_id=user_new_data.id))

# 新しいルートを追加
@app.route("/useself/<int:user_id>")
def show_useself(user_id):
    user = Personal.query.get_or_404(user_id)
    return render_template("useself.html", user=user)

#page3

@app.route("/add_images", methods = ["POST"])
def add_images():
    #db追加
    #場所の名前
    placename = request.form.get("place_name")

    #画像データ
    imagefile = request.files.get("image_file")
    filename = secure_filename(imagefile.filename)
    imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    #db格納
    user_new_date = Question_images(place_name = placename, image_file = filename)
    db.session.add(user_new_date)
    db.session.commit()

    return render_template("choice.html")

#page4

@app.route("/choice")
def choice():
    return render_template("choice.html")





#page5

@app.route("/end")
def end():
    return render_template("end.html")


#実行部分

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)