#import部分


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#定義

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

#db作成

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quesitonnaire_result = db.Column(db.String(50) , unique = True)

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

@app.route("/useself")
def useself():
    return render_template("useself.html")

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