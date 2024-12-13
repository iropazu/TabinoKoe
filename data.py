import sqlite3
import os
import csv

def export_sqlite_to_csv(db_path, output_dir):
    # データベースファイルが存在するか確認
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # データベース内のすべてのテーブル名を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if not tables:
        print("No tables found in the SQLite database.")
        return
    
    # 各テーブルをCSVファイルにエクスポート
    for table_name in tables:
        table_name = table_name[0]  # テーブル名を取得
        output_file = os.path.join(output_dir, f"{table_name}.csv")
        
        # テーブルのデータを取得
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # テーブルのカラム名を取得
        column_names = [description[0] for description in cursor.description]
        
        # CSVファイルに書き込む（日本語対応のエンコーディング）
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # ヘッダーを書き込み
            writer.writerows(rows)  # データを書き込み
        
        print(f"Table '{table_name}' exported to {output_file}")
    
    # 接続を閉じる
    conn.close()
    print("Export completed.")

# 使用例
db_path = "../instance/db.sqlite"  # アップロードされたデータベースファイルのパス
output_dir = "../uploads"  # CSVファイルを格納するディレクトリ
export_sqlite_to_csv(db_path, output_dir)



#input_csv = r"personal.csvファイルのある場所のパスを入力"

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

df = pd.read_csv(input_csv)
df = df.drop(['image_file'], axis=1)
df['user_sex'] = df['user_sex'].astype(str)

sex_counts = df['user_sex'].value_counts()
print(df['user_sex'])
print(sex_counts)
sex_counts.plot.pie(autopct='%1.1f%%', startangle=90, ylabel='')

plt.show()
