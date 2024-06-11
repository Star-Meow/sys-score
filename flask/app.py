#app.py
from flask import Flask,render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import sqlite3,time,datetime
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

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/chips')
def chiph():
    return render_template('chips.html')

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
                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (data['stuid'], '分數減'+ data['score'] + '分', data['info'], nowtime))
            connection.commit()
            connection.close()
            return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route('/party', methods=['POST'])
def party():
    data = request.json
    nowtime = time.strftime("%m-%d %H:%M")
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
                    stu.append(data['member'])
                    sc = 30 + 5 * (int(gp[1]) + 1) 
                    num = []
                    ans = True
                    for i in stu:
                        memA = cursor.execute(
                            "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (i,))
                        mA = memA.fetchone()
                        num.append(mA[2])

                    for i in num:
                        if i <= sc:
                            ans = False
                            break
                    if ans:
                        cursor.execute(
                            "UPDATE team SET ID = ?, mem = ? WHERE Party = ?",
                            (gp[2] + ',' + data['member'] , len(stu), data['gp']))
                        for i, x in enumerate(num):
                            cursor.execute(
                                "UPDATE score SET score = ? WHERE ID = ?",
                                (x - sc , stu[i]))
                            cursor.execute(
                                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                                (stu[i], '追加一位成員，扣除積分', '組隊積分扣除 ' + str(sc), time.strftime("%m-%d %H:%M")))
                            
                        connection.commit()
                        return jsonify({'success': True, "why": "組隊成功!"})
                    else:
                        return jsonify({"success": False, "why": "學生分數不足!"})
                else:
                    return jsonify({"success": False, "why": "找不到此隊伍!"})
            else:
                return jsonify({"success": False, "why": "學生已在隊伍中!"})
        
    elif data['type'] == 3:
        group1 = cursor.execute(
            "SELECT * FROM team WHERE Party = ? ORDER BY ID DESC LIMIT 1", (data['gp1'],))
        gp1 = group1.fetchone()
        group2 = cursor.execute(
            "SELECT * FROM team WHERE Party = ? ORDER BY ID DESC LIMIT 1", (data['gp2'],))
        gp2 = group2.fetchone()    
        if gp1 == None: 
            return jsonify({"success": False, "why": "資料庫找不到隊伍A!"})
        if gp2 == None: 
            return jsonify({"success": False, "why": "資料庫找不到隊伍B!"})
        else:
            stu = gp1[2].split(",")
            stu.extend(gp2[2].split(","))
            sc = 30 + 5 * (int(gp1[1])+int(gp2[1])) 
            num = []
            ans = True
            for i in stu:
                mem = cursor.execute(
                    "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (i,))
                member = mem.fetchone()
                num.append(member[2])
            

            for i in num:
                if i <= sc:
                    ans = False
                    break
            if ans:
                str_stu = ','.join(stu)
                cursor.execute(
                    "UPDATE team SET ID = ?, mem = ? WHERE Party = ?",
                    (str_stu , len(stu), data['gp1']))
                cursor.execute(
                    "DELETE FROM team WHERE party = ?",
                    (data['gp2'],))
                for i, x in enumerate(num):
                    cursor.execute(
                        "UPDATE score SET score = ? WHERE ID = ?",
                        (x - sc , stu[i]))
                    cursor.execute(
                        "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                        (stu[i], '追加一位成員，扣除積分', '組隊積分扣除 ' + str(sc), time.strftime("%m-%d %H:%M")))
                connection.commit()
                
                return jsonify({'success': True, "why": "組隊成功!"})
            else:
                return jsonify({"success": False, "why": "學生分數不足!"})
        

@app.route('/list', methods=['GET'])
def datalist():
    d = int(request.args.get('db'))
    t = int(request.args.get('type'))
    if d is not None:
        if t == 0:
            dbset(d)
            c = cursor.execute("SELECT * FROM score ORDER BY score DESC")
            lst = c.fetchall()
            data = [{
                "id": i[0],
                "name": i[1],
                "score": i[2],
                "chip": i[3]} for i in lst]
            
            return jsonify(data)
        elif t == 1:
            dbset(d)
            c = cursor.execute("SELECT * FROM score ORDER BY chip DESC")
            lst = c.fetchall()
            data = [{
                "id": i[0],
                "name": i[1],
                "score": i[2],
                "chip": i[3]} for i in lst]
            
            return jsonify(data)

    else:
        return jsonify({"error": "db parameter is missing"}), 400


@app.route('/bid', methods=['POST'])
def bid():
    data = request.json


    dbset(int(data['db']))
    if data['type'] == 1:
        deadline1 = "2024/06/07"
        deadline2 = "2024/06/10"
        nowtime = time.strftime("%y/%m/%d")
        if deadline2 > nowtime:
            if deadline1 > nowtime:
                ratio = 2
            else:
                ratio = 1
        else:
            ratio = 0.5

        c = cursor.execute(
            "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1",(data['ID'],))
        stu = c.fetchone()
        if stu[2] >= int(data['score']):
            chipadd = int(int(data['score'])*ratio)
            if stu[3] == None:
                cursor.execute(
                    "UPDATE score SET score = ?, chip = ? WHERE ID = ?",
                    (stu[2]-int(data['score']) , chipadd, data['ID']))
                cursor.execute(
                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                    (data['ID'], "消耗積分"+ str(data['score']) + '倍率為 '+ str(ratio)+ "倍", "籌碼兌換", nowtime))
                connection.commit()
                connection.close()
                return jsonify({'success': True})
            else:
                cursor.execute(
                    "UPDATE score SET score = ?, chip = ? WHERE ID = ?",
                    (stu[2]-int(data['score']) , chipadd + stu[3], data['ID']))
                cursor.execute(
                "INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)",
                    (data['ID'], "消耗積分"+ str(data['score']) + '倍率為 '+ str(ratio)+ "倍", "籌碼兌換", nowtime))
                connection.commit()
                connection.close()
                return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    if data['type'] == 2: 
        c = cursor.execute(
            "SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1",(data['bidder'],))
        stu = c.fetchone()
        if stu[3] >=  int(data['bid']):
            cursor.execute(
            "INSERT INTO bid (tema, bidder, bid) VALUES (?, ?, ?)",
                (data['tema'],data['bidder'],data['bid']))
            cursor.execute(
                "UPDATE score SET chip = ? WHERE ID = ?",
                (stu[3]- int(data['bid']), data['bidder']))
            
            connection.commit()

            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "why": "分數不足買下標物"})  
    else:
        return jsonify({'success': False})       


@app.route('/tema', methods=['GET'])
def tema():
    d = int(request.args.get('db'))
    t = int(request.args.get('type'))

    if d is not None:
        if t == 0:
            dbset(d)
            c = cursor.execute("SELECT * FROM team ORDER BY Party")
            lst = c.fetchall()
            data = [{
                "party": i[0],
                "count": i[1],
                "member": i[2],} for i in lst]
            
            return jsonify(data)
        elif t == 1:
            dbset(d)
            c = cursor.execute("SELECT * FROM bid ORDER BY bidder")
            lst = c.fetchall()
            data = [{
                "tema": i[0],
                "bidder": i[1],
                "bid": i[2],} for i in lst]
            
            return jsonify(data)

    else:
        return jsonify({"error": "db parameter is missing"}), 400



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5050 )
