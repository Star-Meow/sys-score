#app.py
from flask import Flask,render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import sqlite3,time
from time import sleep


app = Flask(__name__)
app.secret_key = 'suzuran'
cors = CORS(app)
db_config = {
    'database': 'logic2A.db' 
}

def dbset(value):
    global db_config, connection, cursor
    
    values=["遊戲程式邏輯2A", "遊戲程式邏輯2B", "互動媒體設計2A","互動媒體設計2B"]
    if value == 0:
        db_config = {
        'database': '.\static\database\logic2A.db' 
    }
    elif value == 1:
        db_config = {
        'database': '.\static\database\logic2B.db' 
    }
    elif value == 2:
        db_config = {
        'database': '.\static\database\media2A.db' 
    }
    elif value == 3:
        db_config = {
        'database': '.\static\database\media2B.db' 
    }
    while True:
        try:
            connection = sqlite3.connect(**db_config)
            cursor = connection.cursor()

            print("成功連接至DB！")
            break
        except sqlite3.Error as e:
            print(f"連接錯誤: {e}")
            print("reconneciton...")
            sleep(2)
    print(db_config)

@app.route('/')
def index():
    return render_template('Create.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        nowtime = time.strftime("%m-%d %H:%M")
        print(data)

        dbset(int(data['db']))
        if data['symbol'] == '+':
            c = cursor.execute(
                "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (data['stuid'],))
            point = c.fetchone()
            p = point[2]
            p += int(data['score'])
            c = cursor.execute(
                "UPDATE score SET score = ? WHERE ID = ?", (p, data['stuid']))
            cursor.execute(
                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (data['stuid'], '分數加'+ data['score'] + '分', data['info'], nowtime))
            connection.commit()
            connection.close()
            return jsonify({'success': True})
        elif data['symbol'] == '-':
            c = cursor.execute(
                "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (data['stuid'],))
            point = c.fetchone()
            p = point[2]
            p -= int(data['score'])
            c = cursor.execute(
                "UPDATE score SET score = ? WHERE ID = ?", (p, data['stuid']))
            cursor.execute(
                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (data['stuid'], '分數加'+ data['score'] + '分', data['info'], nowtime))
            connection.commit()
            connection.close()
            return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/party', methods=['POST'])
def party():
    data = request.json
    nowtime = time.strftime("%m-%d %H:%M")
    print(data)
    dbset(int(data['db']))
    if data['type'] == 1:
        if data['memberA'] != data['memberB']:
            memA = cursor.execute(
                "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (data['memberA'],))
            mA = memA.fetchone()
            memB = cursor.execute(
                "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (data['memberB'],))
            mB = memB.fetchone()    
            if mA == None or mB == None:
                return jsonify({"success": False, "why": "資料庫找不到該學生!"})
            else:
                c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + str(data['memberA']) + '%',))
                stu1 = c.fetchone()
                c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + str(data['memberB']) + '%',))
                stu2 = c.fetchone()

                if stu1 == None and stu2 == None:
                    if mA[2] > 40 and mB[2] > 40:

                        c = cursor.execute("SELECT MAX(Party) FROM team")
                        p_max = c.fetchone()
                        p = 0
                        if p_max[0] == None:
                            p = 1
                        else:
                            p = int(p_max[0]) + 1

                        cursor.execute(
                            "INSERT INTO team (Party, mem, ID) VALUES (?, ?, ?)", 
                            (p  ,2 , data['memberA'] + ',' + data['memberB']))
                        cursor.execute(
                            "UPDATE score SET score = ? WHERE ID = ?",
                            (mA[2]-40 , data['memberA']))
                        cursor.execute(
                            "UPDATE score SET score = ? WHERE ID = ?",
                            (mB[2]-40 , data['memberA']))
                        cursor.execute(
                            "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                            (data['memberA'], '兩人組隊扣除積分', '組隊積分扣除 40', time.strftime("%m-%d %H:%M")))
                        cursor.execute(
                            "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                            (data['memberB'], '兩人組隊扣除積分', '組隊積分扣除 40', time.strftime("%m-%d %H:%M")))
                        
                        connection.commit()
                        return jsonify({'success': True, "why": "組隊成功!"})
                    else:
                        return jsonify({"success": False, "why": "學生分數不足!"})
                else:
                    return jsonify({"success": False, "why": "學生已在隊伍中!"})
        else:
            return jsonify({"success": False, "why": "學號重複!"})
                
    elif data['type'] == 2:
        member = cursor.execute(
            "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (data['member'],))
        mem = member.fetchone()
        group = cursor.execute(
            "SELECT * FROM team WHERE Party = ? ORDER BY ID DESC LIMIT 1", (data['gp'],))
        gp = group.fetchone()    
        if mem == None: 
            return jsonify({"success": False, "why": "資料庫找不到該學生!"})
        if gp == None: 
            return jsonify({"success": False, "why": "資料庫找不到該隊伍!"})
        else:
            c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + str(data['member']) + '%',))
            stu1 = c.fetchone()

            if stu1 == None:
                if gp != None:
                    stu = gp[2].split(",")
                    sc = 30 + 5 * (int(gp[1]) + 1) 
                    
                    memA = cursor.execute(
                        "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (stu[0],))
                    mA = memA.fetchone()
                    memB = cursor.execute(
                        "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (stu[1],))
                    mB = memB.fetchone()
                    if mA[2] > 40 and mB[2] > 40:

                        return jsonify({'success': True, "why": "組隊成功!"})
                    else:
                        return jsonify({"success": False, "why": "學生分數不足!"})
                else:
                    return jsonify({"success": False, "why": "找不到此隊伍!"})
            else:
                return jsonify({"success": False, "why": "學生已在隊伍中!"})
        
    elif data['type'] == 3:
        return jsonify({'success': True})
    else:
        return jsonify({"success": False, "why": "學生已在隊伍中!"})


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5050 )
