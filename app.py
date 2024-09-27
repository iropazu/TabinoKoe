from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_title = db.Column(db.String(50) , unique = True)
    post = db.Column(db.String(200) , unique = True)

@app.route("/")
def home():
    return render_template("Index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)