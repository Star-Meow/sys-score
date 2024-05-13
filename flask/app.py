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
    try:
        data = request.json
        nowtime = time.strftime("%m-%d %H:%M")
        print(data)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000 )