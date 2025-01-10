#import部分
from itsdangerous import URLSafeSerializer
import json
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os
import uuid


#定義

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
secret_key = 'your-secret-key-here'  
serializer = URLSafeSerializer(secret_key)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # ログインページのエンドポイントを指定

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))


#db作成

class Personal(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_ages = db.Column(db.String(100))
    user_sex = db.Column(db.String(100))
    user_place = db.Column(db.String(100))
    place_name = db.Column(db.String(100))
    image_file = db.Column(db.String(100))
    know_place = db.Column(db.String(100))
    count_kanazawa = db.Column(db.String(100))
    favorite_activity = db.Column(db.String(1999))
    additional_comments = db.Column(db.String(1999))

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)  # ユーザーがアクティブかどうかを示すフィールド

    @property
    def is_active(self):
        return self.active  

    def get_id(self):
        return self.id  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

##HomePage

@app.route("/")
def home():
    return render_template("main.html")

##アンケート部分

#page1

@app.route("/home", methods = ['GET'])
def question_home():
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

@app.route("/add_texts/<encrypted_id>", methods = ["POST"])
def add_texts(encrypted_id):
    try:
        # 暗号化されたIDを復号化
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)

        # フォームデータの取得
        know_place = request.form.get("know_place")
        count_kanazawa = request.form.get("count_kanazawa")
        favorite_activity = request.form.get("favorite_activity")
        additional_comments = request.form.get("additional_comments")

        #dbを更新
        user.know_place = know_place
        user.count_kanazawa = count_kanazawa
        user.favorite_activity = favorite_activity
        user.additional_comments = additional_comments
        db.session.commit()

        return redirect(url_for('end', encrypted_id=encrypted_id))
    except:
        return abort(404)





#page5

@app.route("/end/<encrypted_id>")
def end(encrypted_id):
    try:
        # 暗号化されたIDを復号化して確認
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)
        return render_template("end.html", user=user, encrypted_id=encrypted_id)
    except Exception as e:
        print(f"Error in add_images: {str(e)}")
        return abort(404)
    
    
    
@app.route("/gurahu")
def kaiseki():
    db_path = r"C:\Users\youic\Desktop\2024後期\PD実践\instance\db.sqlite"  # データベースのパス
    query = "SELECT * FROM table_name"  # 実際のクエリに置き換えてください
    data = fetch_data_from_sql(db_path, query)
    return data.to_html()
    
    



@app.route("/display/<encrypted_id>")
def display(encrypted_id):
    try:
        # 暗号化されたIDを復号化して確認
        user_id = serializer.loads(encrypted_id)
        user = Personal.query.get_or_404(user_id)
        
        # ランダムな推薦を取得
        recommendation = Recommendation.query.order_by(db.func.random()).first()
        
        return render_template("display.html", user=user, encrypted_id=encrypted_id, recommendation=recommendation)
    except Exception as e:
        print(f"Error in display: {str(e)}")
        return abort(404)


#SNS部分


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ユーザー名の重複チェック
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        # 新しいユーザーの作成
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))  # ログインページにリダイレクト
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))  # ログイン後のリダイレクト先
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


#実行部分

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # テーブルが空の場合、ダミーデータを追加
        if not Recommendation.query.first():
            dummy_data = [
                Recommendation(place_name="東京タワー", image_file="tokyo_tower.jpg"),
                Recommendation(place_name="富士山", image_file="mount_fuji.jpg"),
                Recommendation(place_name="京都寺院", image_file="kyoto_temple.jpg")
            ]
            db.session.bulk_save_objects(dummy_data)
            db.session.commit()
        
    app.run(debug=True)