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
    user_ages = db.Column(db.String(100) , unique = True)
    user_sex = db.Column(db.String(100) , unique = True)
    user_place = db.Column(db.String(100) , unique = True)

class choiceanswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    how_known = db.Column(db.String(100))
    visit_count = db.Column(db.String(100))
    visit_reason = db.Column(db.Text)
    inconvenience = db.Column(db.Text)
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
    user_new_data = Questionnaire(user_ages = userages, user_sex = usersex, user_place = userplace)
    db.session.add(user_new_data)
    db.session.commit()


    return render_template("useself.html")

#page3



#page4

@app.route("/choice",methods = ["GET","POST"])
def choice():
    if request.method == "POST":
        # フォームデータの取得
        how_known = request.form.get("how_known")
        visit_count = request.form.get("visit_count")
        visit_reason = request.form.get("visit_reason")
        inconvenience = request.form.get("inconvenience")

        # 最新のユーザーレコードを取得して更新
        latest_user = Questionnaire.query.order_by(Questionnaire.id.desc()).first()
        if latest_user:
            latest_user.how_known = how_known
            latest_user.visit_count = visit_count
            latest_user.visit_reason = visit_reason
            latest_user.inconvenience = inconvenience
            db.session.commit()

        return redirect(url_for('choice'))
    if request.method == "GET":
        return render_template("end.html")





#page5

@app.route("/end")
def end():
    return render_template("end.html")


#実行部分

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)