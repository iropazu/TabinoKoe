#import部分


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

class Question_images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quesitonnaire_result = db.Column(db.String(50) , unique = True)
    place_name = db.Column(db.String(10), nullable = False)
    image_file = db.Column(db.String(100), nullable = False)

##アンケート部分

#page1

@app.route("/home")
def home():
    return render_template("home.html")

#page2

@app.route("/information")
def information():
    return render_template("information.html")

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