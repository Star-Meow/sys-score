import pandas as pd
import sqlite3

# 假設使用SQLite資料庫，請根據實際資料庫類型修改
database_files = {
    "遊戲程式邏輯2A": ".\static\database\logic2A.db",
    "遊戲程式邏輯2B": ".\static\database\logic2B.db",
    "互動媒體設計2A": ".\static\database\media2A.db",
    "互動媒體設計2B": ".\static\database\media2B.db"
}

output_path = ".\static\out_excel\積分表.xlsx"

# 創建一個ExcelWriter對象
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for course, db_file in database_files.items():
        # 連接資料庫
        conn = sqlite3.connect(db_file)
        
        # 讀取score表中的資料
        query = "SELECT * FROM score"
        df = pd.read_sql_query(query, conn)
        
        # 關閉資料庫連接
        conn.close()
        
        # 將DataFrame儲存為Excel文件中的一個工作表
        sheet_name = course
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"已將 {course} 的資料儲存到工作表 {sheet_name}")

print(f"所有資料已成功匯出到Excel文件 {output_path}")
