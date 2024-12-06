import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# データベース接続
def fetch_data_from_sql(link, query):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(link)
        # クエリ実行
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"エラー: {e}")
        return None

# グラフ作成
def plot_data(df, x_column, y_column, plot_type="line"):
    try:
        if plot_type == "line":
            df.plot(x=x_column, y=y_column, kind="line")
        elif plot_type == "bar":
            df.plot(x=x_column, y=y_column, kind="bar")
        elif plot_type == "scatter":
            df.plot(x=x_column, y=y_column, kind="scatter")
        else:
            print("対応していないグラフ形式です。")
            return
        
        plt.title("SQL Data Visualization")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"グラフ作成エラー: {e}")

# 使用例
if __name__ == "__main__":
    # データベース名とクエリを指定
    database_name = "example.db"
    sql_query = "SELECT date, value FROM sample_table;"  # 適切なクエリを指定
    data = fetch_data_from_sql(database_name, sql_query)
    
    if data is not None:
        print(data.head())  # データを確認
        # データをグラフ化
        plot_data(data, x_column="date", y_column="value", plot_type="line")
