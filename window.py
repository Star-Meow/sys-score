from pathlib import Path
import sqlite3, random
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import ttk,Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import time
from time import sleep
OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")
def asset_win1(path: str) -> Path:
    return ASSETS_PATH / Path(path)


db_config = {
    'database': './flask/static/database/logic2A.db'
}

def dbset():
    global db_config, connection, cursor
    eclass = entry_class.get()
    values=["遊戲程式邏輯2A", "遊戲程式邏輯2B", "互動媒體設計2A","互動媒體設計2B"]
    if eclass == values[0]:
        db_config = {
        'database': './flask/static/database/logic2A.db' 
    }
    elif eclass == values[1]:
        db_config = {
        'database': './flask/static/database/logic2B.db' 
    }
    elif eclass == values[2]:
        db_config = {
        'database': './flask/static/database/media2A.db' 
    }
    elif eclass == values[3]:
        db_config = {
        'database': './flask/static/database/media2B.db' 
    }
    print(db_config)
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


def sent_btn():
    nowtime = time.strftime("%m-%d %H:%M")
    dbset()
    eclass = entry_class.get()
    id = entry_name.get()
    action = entry_action.get()
    info = entry_info.get()
    entry_check = [
        eclass,
        id,
        action,
    ]
    if all(entry_check):
        try:


            if action[0] in ['+', '-', '*', '/'] or action[0].isdigit():
                if action[1:].isdigit():
                    c = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (id,))
                    r = c.fetchone()
                    if r:
                        if action[0] == '-':
                            new_score = r[2] - int(action[1:])
                            act = '分數扣 '+ action[1:] + ' 分'
                        elif action[0] == '*':
                            new_score = r[2] * int(action[1:])
                            act = '分數乘以 '+ action[1:] 
                        elif action[0] == '/':
                            new_score = r[2] // int(action[1:])
                            act = '分數除以 '+ action[1:]
                        else:
                            new_score = r[2] + int(action)
                            if  action[0].isdigit():
                                act = '分數加 '+ action[0:] + ' 分'
                            else:
                                act = '分數加 '+ action[1:] + ' 分'

                        if new_score < 0:
                            new_score = 0
                        cursor.execute("UPDATE score SET score = ? WHERE ID = ?", (new_score, id))
                        cursor.execute("INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (id, act, info, nowtime))

                        print(f"{r[2]}，修改為 {new_score}！")
                        messagebox.showinfo("更改成功",f"學生 {r[1]} 經過{act}後,分數目前為{new_score}！")
                        connection.commit()
                    else:
                        messagebox.showerror("error",'請檢查學號以及課程有無錯誤')
                        print("更新資料失敗")
                
                else:
                    messagebox.showerror("error",'請檢查分數欄位是否有錯')
                    print('中間請不要插入其他符號')
            else:
                messagebox.showerror("error",'數字前面只能由+ - * / 開頭 ,加分可不用加號')
                print('數字前面只能由+-*/開頭 ,加分可不用加號')
                
        except sqlite3.Error as e:
            messagebox.showerror("錯誤", f"執行 SQL 查詢時出錯: {e}")
            print(f"執行 SQL 查詢時出錯: {e}")
    else:
        messagebox.showerror("error","課程,學號,分數皆不能為空")
        print("課程,學號,分數皆不能為空")
    entry_contents = [
        entry_class.get(),
        entry_name.get(),
        entry_action.get(),
        entry_info.get(),  
    ]
    print("Entry框的內容:")
    for content in entry_contents:
        print(content)
    print(db_config)


window = Tk() #分數視窗
window.geometry("500x700") 
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 700,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    500.0,
    700.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    500.0,
    53.33333206176758,
    fill="#919191",
    outline="")

class_image = PhotoImage(
    file=asset_win1("entry_4.png"))
entry_bg_4 = canvas.create_image(
    250.0,
    132.0,
    image=class_image
)
entry_class = ttk.Combobox(
    values=["遊戲程式邏輯2A", "遊戲程式邏輯2B", "互動媒體設計2A","互動媒體設計2B"],  # Set the values for the combobox
    state="readonly",  # Make the combobox read-only
    style="Combobox.TCombobox",  # Set the style for the combobox
)
entry_class.place(
    x=50.0,
    y=111.0,
    width=400.0,
    height=40.0
)

name_image = PhotoImage(
    file=asset_win1("entry_2.png"))
entry_bg_2 = canvas.create_image(
    250.0,
    267.0,
    image=name_image 
)
entry_name = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_name.place(
    x=50.0,
    y=246.0,
    width=400.0,
    height=40.0
)

action_image = PhotoImage(
    file=asset_win1("entry_3.png"))
entry_bg_3 = canvas.create_image(
    250.0,
    402.0,
    image=action_image 
)
entry_action = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_action.place(
    x=50.0,
    y=381.0,
    width=400.0,
    height=40.0
)

info_image = PhotoImage(
    file=asset_win1("entry_1.png"))
entry_bg_1 = canvas.create_image(
    250.0,
    537.0,
    image=info_image
)
entry_info= Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_info.place(
    x=50.0,
    y=516.0,
    width=400.0,
    height=40.0
)

button_image_1 = PhotoImage(
    file=asset_win1("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=sent_btn,
    relief="flat"
)
button_1.place(
    x=160.0,
    y=620.0,
    width=181.0,
    height=40.0
)

canvas.create_text(
    50.0,
    351.0,
    anchor="nw",
    text="score\n",
    fill="#000000",
    font=("Inter", 20 * -1)
)
canvas.create_text(
    50.0,
    493.0,
    anchor="nw",
    text="info\n",
    fill="#000000",
    font=("Inter", 20 * -1)
)
canvas.create_text(
    50.0,
    223.0,
    anchor="nw",
    text="ID",
    fill="#000000",
    font=("Inter", 20 * -1)
)
canvas.create_text(
    50.0,
    88.0,
    anchor="nw",
    text="Class",
    fill="#000000",
    font=("Inter", 20 * -1)
)
canvas.create_text(
    225.0,
    16.0,
    anchor="nw",
    text="系統",
    fill="#000000",
    font=("Inter", 20 * -1)
)

if __name__ == '__main__':
    window.resizable(False, False)
    window.mainloop()