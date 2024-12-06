import matplotlib.pyplot as plt
import io
import base64
from flask import app, abort

# グラフ表示エンドポイント
@app.route("/graph")
def display_graph():
    try:
        # データベースから全てのデータを取得
        all_data = Personal.query.all()

        # データの集計 (例: 性別ごとの人数)
        sex_count = {}
        for entry in all_data:
            sex = entry.user_sex
            if sex in sex_count:
                sex_count[sex] += 1
            else:
                sex_count[sex] = 1

        # グラフ作成
        fig, ax = plt.subplots()
        ax.bar(sex_count.keys(), sex_count.values(), color='skyblue')
        ax.set_title('User Distribution by Sex')
        ax.set_xlabel('Sex')
        ax.set_ylabel('Count')

        # グラフを画像としてエンコード
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close(fig)

        # 画像をBase64エンコードしてHTMLで表示
        graph_url = base64.b64encode(img.getvalue()).decode()
        graph_html = f"<img src='data:image/png;base64,{graph_url}'/>"
        return graph_html
    except Exception as e:
        print(f"Error creating graph: {e}")
        return abort(500)
