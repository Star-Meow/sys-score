import sqlite3, random, datetime
from time import sleep

db_config = {
    'database': 'stu.db' 
}
 
def tryconnection():
    global connection, cursor
    while True:
        try:
            connection = sqlite3.connect(**db_config)
            cursor = connection.cursor()

            print("成功連接至DB！")
            break
        except sqlite3.Error as e:
            print(f"連接錯誤: {e}")
            print("reconneciton...")
            sleep(5)




def stu(frame):
    tryconnection()

    try:
        c = cursor.execute("select * from players order by NO desc LIMIT 1")
        r = c.fetchone()
        data = (frame)
        KEY = 0
        if r is not None:
            if len(r) == 0:
                KEY = 1
            else:
                KEY = r[0] + 1
        else:
            KEY = 1
        for i in range(10):
            cursor.execute(
                "INSERT INTO players (NO, number, has_ball, x_coor, y_coor, DATETIME) VALUES (?, ?, ?, ?, ?, ?)",
                (KEY+i, data[0][i], data[1][i], data[2][i], data[3][i],frame))
            print(f"成功加入 NO:{KEY+i} number: {data[0][i]}, 持球:{data[1][i]}, X座標:{data[2][i]}, Y座標{data[3][i]},禎數:{frame}")

    connection.commit()  # 提交更改
    sleep(1)

def update_score(No, score, info, action):
    c.execute("UPDATE stu SET score=?, info=?, action=? WHERE No=?", (score, info, action, No))
    conn.commit()
    print("分數更新成功！")

if __name__ == '__main__':
    fakedata()