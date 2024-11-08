#import部分
from itsdangerous import URLSafeSerializer
import json
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

#定義

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
secret_key = 'your-secret-key-here'  # 実際の運用では環境変数などから安全に読み込むことを推奨
serializer = URLSafeSerializer(secret_key)
db = SQLAlchemy(app)


#db作成

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_ages = db.Column(db.String(100))
    user_sex = db.Column(db.String(100))
    user_place = db.Column(db.String(100))
    place_name = db.Column(db.String(100))
    image_file = db.Column(db.String(100))

##アンケート部分

#page1

@app.route("/home")
def home():
    return render_template("home.html")

#page2

@app.route("/information", methods=['GET'])
def show_form():
    try:
        # 絶対パスを使用
        base_dir = os.path.abspath(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'static', 'prefectures.json')
        
        # デバッグ用のプリント
        print(f"Looking for JSON file at: {json_path}")
        print(f"File exists: {os.path.exists(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('information.html', prefectures=data['prefectures'])
    except Exception as e:
        # エラーの詳細をログに出力
        print(f"Error loading JSON: {str(e)}")
        return str(e), 500  # エラーメッセージをブラウザに表示

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

    # IDを暗号化
    encrypted_id = serializer.dumps(user_new_data.id)
    return redirect(url_for('show_useself', encrypted_id=encrypted_id))

@app.route("/useself/<encrypted_id>")
def show_useself(encrypted_id):
    try:
        # 暗号化されたIDを復号化
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)
        return render_template("useself.html", user=user, encrypted_id=encrypted_id)
    except Exception as e:
        # 不正なIDの場合は404を返す
        print(f"Error in show_useself: {str(e)}")
        return abort(404)

#page3

@app.route("/add_images/<encrypted_id>", methods=["POST"])
def add_images(encrypted_id):
    try:
        # 暗号化されたIDを復号化
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)

        # フォームデータの取得
        placename = request.form.get("place_name")
        imagefile = request.files.get("image_file")
        
        if imagefile:
            filename = secure_filename(imagefile.filename)
            imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # 既存のユーザーレコードを更新
            user.place_name = placename
            user.image_file = filename
            db.session.commit()

        return redirect(url_for('choice', encrypted_id=encrypted_id))
    except:
        return abort(404)

#page4

@app.route("/choice/<encrypted_id>")
def choice(encrypted_id):
    try:
        # 暗号化されたIDを復号化して確認
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)
        return render_template("choice.html", user=user, encrypted_id=encrypted_id)
    except Exception as e:
        print(f"Error in add_images: {str(e)}")
        return abort(404)





#page5

@app.route("/end")
def end():
    return render_template("end.html")


#実行部分

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)