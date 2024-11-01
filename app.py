#import部分


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#定義

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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

@app.route("/information")
def information():
    return render_template("information.html")

@app.route("/useself", methods = ["POST"])
def add():
    ##db追加
    #年齢
    userages = request.form.get("user_ages")

    #性別
    usersex = request.form.get("sex")

    #出身地
    userplace = request.form.get("place")

    #db格納
    user_new_data = Personal(user_ages = userages, user_sex = usersex, user_place = userplace)
    db.session.add(user_new_data)
    db.session.commit()


    return render_template("useself.html")

#page3



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