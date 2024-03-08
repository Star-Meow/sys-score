import pandas as pd
import sqlite3

file = ["互動媒體設計2A.xlsx", "互動媒體設計2B.xlsx", "遊戲程式邏輯2A.xlsx", "遊戲程式邏輯2B.xlsx"]

path = [r'E:\github\sys-score\media2A.db', r'E:\github\sys-score\media2B.db', r'E:\github\sys-score\logic2A.db', r'E:\github\sys-score\logic2B.db']
for i in range(len(file)):
    df = pd.read_excel(file[i])
    df = df.iloc[3:, :3]  # 從第5行到結束，提取前三列

    
    db_path = path[i]
    conn = sqlite3.connect(db_path)

    try:
        df.columns = ["ID", "name", "score"]
        df.to_sql("score", conn, if_exists="replace", index=False)
        print("資料寫入成功！")
    except Exception as e:
        print(f"寫入資料庫時出現錯誤: {e}")

    conn.close()
