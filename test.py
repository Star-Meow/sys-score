import sqlite3

def copy_data_and_modify_table(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # 將A資料表的ID和name複製至B資料表
    cursor.execute("INSERT INTO stu (ID, name) SELECT ID, name FROM score")

    cursor.execute("CREATE TABLE point AS SELECT ID, score FROM score")
    cursor.execute("DROP TABLE score")
    cursor.execute("ALTER TABLE point RENAME TO score")
    cursor.execute("COMMIT")

    conn.commit()
    conn.close()

# 使用範例
if __name__ == "__main__":
    database_name = "bestuse.db"  # 更換成你的SQLite資料庫檔案名稱
    copy_data_and_modify_table(database_name)