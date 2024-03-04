from pathlib import Path
import sqlite3, random
from tkinter import ttk,Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import time
from time import sleep
# en_1 -> 左下 此次新增隊員,en_2 -> memberB ,en_3 -> 左下 組別 ,en_4 -> 右上組別A ,en_5 -> memberA ,en_6 -> 課程box 


def asset_win2(path: str) -> Path:
    OUTPUT_PATH2 = Path.cwd()
    ASSETS_PATH2 = OUTPUT_PATH2 / Path("assets/frame1")
    return ASSETS_PATH2 / Path(path)

def dbset():
    global db_config, connection, cursor
    eclass = entry_6.get()
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

def btn_build():#建組
    dbset()
    classes = entry_6.get()
    memberA = entry_5.get()
    memberB = entry_2.get()
    memA = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (memberA,))
    memB = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (memberB,))
    rA = memA.fetchone()
    rB = memB.fetchone()
    a_s = rA[2] - 40
    b_s = rB[2] - 40
    print(classes,'A:'+memberA,'B:'+memberB,a_s,b_s)
    
def btn_add():#增員
    print('')

def btn_merge(): #合併
    print('')

def btn_query():#查詢
    print('')

teamwindow = Tk()

teamwindow.geometry("1080x800")
teamwindow.configure(bg="#FFFFFF")


canvas = Canvas(
    teamwindow,
    bg="#FFFFFF",
    height=800,
    width=1080,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    1080.0,
    800.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1080.0,
    53.0,
    fill="#919191",
    outline="")

entry_image_1 = PhotoImage(
    file=asset_win2("entry_1.png"))
entry_bg_1 = canvas.create_image(
    250.0,
    669.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=50.0,
    y=648.0,
    width=400.0,
    height=40.0
)

entry_image_2 = PhotoImage(
    file=asset_win2("entry_2.png"))
entry_bg_2 = canvas.create_image(
    256.0,
    370.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
)
entry_2.place(
    x=56.0,
    y=349.0,
    width=400.0,
    height=40.0
)
entry_2.insert(0, '109021071')

entry_image_3 = PhotoImage(
    file=asset_win2("entry_3.png"))
entry_bg_3 = canvas.create_image(
    250.0,
    578.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=50.0,
    y=557.0,
    width=400.0,
    height=40.0
)

entry_image_4 = PhotoImage(
    file=asset_win2("entry_4.png"))
entry_bg_4 = canvas.create_image(
    749.0,
    180.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=549.0,
    y=159.0,
    width=400.0,
    height=40.0
)

entry_image_5 = PhotoImage(
    file=asset_win2("entry_5.png"))
entry_bg_5 = canvas.create_image(
    256.0,
    272.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=56.0,
    y=251.0,
    width=400.0,
    height=40.0
)
entry_5.insert(0, '109021071')

entry_image_6 = PhotoImage(
    file=asset_win2("entry_6.png"))
entry_bg_6 = canvas.create_image(
    256.0,
    125.0,
    image=entry_image_6
)
entry_6 = ttk.Combobox(
    values=["遊戲程式邏輯2A", "遊戲程式邏輯2B", "互動媒體設計2A","互動媒體設計2B"],  
    state="readonly", 
    style="Combobox.TCombobox", 
)
entry_6.place(
    x=56.0,
    y=104.0,
    width=400.0,
    height=40.0
)

button_image_1 = PhotoImage(
    file=asset_win2("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= btn_build,
    relief="flat"
)
button_1.place(
    x=50.0,
    y=417.0,
    width=181.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=asset_win2("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=549.0,
    y=330.0,
    width=181.0,
    height=40.0
)

button_image_3 = PhotoImage(
    file=asset_win2("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=766.0,
    y=531.0,
    width=181.0,
    height=40.0
)

button_image_4 = PhotoImage(
    file=asset_win2("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=50.0,
    y=727.0,
    width=181.0,
    height=40.0
)

canvas.create_text(
    50.0,
    625.0,
    anchor="nw",
    text="此次新增隊員",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    50.0,
    534.0,
    anchor="nw",
    text="組別",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    56.0,
    228.0,
    anchor="nw",
    text="隊員A - 學號",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    549.0,
    136.0,
    anchor="nw",
    text="組別A",
    fill="#000000",
    font=("Inter", 20 * -1)
)

entry_image_7 = PhotoImage(
    file=asset_win2("entry_7.png"))
entry_bg_7 = canvas.create_image(
    749.0,
    484.0,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_7.place(
    x=549.0,
    y=463.0,
    width=400.0,
    height=40.0
)

canvas.create_text(
    549.0,
    440.0,
    anchor="nw",
    text="組別",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    549.0,
    539.0,
    anchor="nw",
    text="組別人員為:",
    fill="#000000",
    font=("Inter", 20 * -1)
)

entry_image_8 = PhotoImage(
    file=asset_win2("entry_8.png"))
entry_bg_8 = canvas.create_image(
    749.0,
    272.0,
    image=entry_image_8
)
entry_8 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_8.place(
    x=549.0,
    y=251.0,
    width=400.0,
    height=40.0
)

canvas.create_text(
    549.0,
    228.0,
    anchor="nw",
    text="組別B",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    56.0,
    325.0,
    anchor="nw",
    text="隊員B - 學號",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    56.0,
    179.0,
    anchor="nw",
    text="新增隊伍 - (two man cell)",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    549.0,
    93.0,
    anchor="nw",
    text="隊伍合併 - (兩隻兩人隊伍以上)",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    56.0,
    81.0,
    anchor="nw",
    text="課程選擇 *",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    549.0,
    400.0,
    anchor="nw",
    text="隊伍查詢",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    50.0,
    489.0,
    anchor="nw",
    text="新增隊員 - (兩人以上) ",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    476.0,
    15.0,
    anchor="nw",
    text="組隊用介面",
    fill="#000000",
    font=("Inter", 20 * -1)
)
teamwindow.resizable(False, False)
teamwindow.mainloop()