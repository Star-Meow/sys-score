from flask import Flask,render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'suzuran'


db_config = {
    'database': 'logic2A.db' 
}

def dbset():
    global db_config, connection, cursor
    eclass = ''
    values=["遊戲程式邏輯2A", "遊戲程式邏輯2B", "互動媒體設計2A","互動媒體設計2B"]
    if eclass == values[0]:
        db_config = {
        'database': 'logic2A.db' 
    }
    elif eclass == values[1]:
        db_config = {
        'database': 'logic2B.db' 
    }
    elif eclass == values[2]:
        db_config = {
        'database': 'media2A.db' 
    }
    elif eclass == values[3]:
        db_config = {
        'database': 'media2B.db' 
    }
        

@app.route('/')
def index():
    return render_template('Create.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print(data)
    session['score'] = data['score']
    return jsonify(data)

@app.route('/data')
def data():
    data = session.get('score')

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)