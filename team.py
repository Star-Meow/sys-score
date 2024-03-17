from pathlib import Path
import sqlite3, random
from tkinter import ttk,Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import time
from time import sleep
# en_1 -> 左下 此次新增隊員 
#en_2 -> memberB 
#en_3 -> 左下 組別 
#en_4 -> 右上組別A 
#en_5 -> memberA 
#en_6 -> 課程box 
#en_7 -> 右下Query


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
    try:
        memA = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (memberA,))
        rA = memA.fetchone()
        memB = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (memberB,))
        rB = memB.fetchone()

        id_A = [int(rA[0]) ,int(rA[2])]#學號,分數
        id_B = [int(rB[0]) ,int(rB[2])]
        

    except:
        messagebox.showerror("錯誤","輸入的學號不存在，請檢查")
        print("學號不存在，請檢查錯誤")


    if id_A[0] == id_B[0]: #先檢查學號
        messagebox.showerror("組隊失敗","兩人學號相同")
        print("兩個學號一樣")
        print(classes,'A:'+memberA,'B:'+memberB,rA,rB)
    else:#再查看分數
        c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + str(id_A[0]) + '%',))
        ser1 = c.fetchone()
        c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + str(id_B[0]) + '%',))
        ser2 = c.fetchone()
        print(ser1,ser2)
        if ser1 == None and ser2 == None:
            if rA[2] - 40 >= 0 and  rB[2] - 40 >= 0 :
                c = cursor.execute("SELECT MAX(Party) FROM team")
                n_p = c.fetchone()

                cursor.execute("INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (id_A[0], '兩人組隊扣除積分', '組隊積分扣除 40', time.strftime("%m-%d %H:%M")))
                cursor.execute("INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (id_B[0], '兩人組隊扣除積分', '組隊積分扣除 40', time.strftime("%m-%d %H:%M")))
                if n_p[0] == None:
                    pt = 1
                else:
                    pt = int(n_p[0]) + 1
                cursor.execute("INSERT INTO team (Party, mem, ID) VALUES (?, ?, ?)", (pt  ,2 ,str(id_A[0]) + ',' + str(id_B[0])))
                cursor.execute("UPDATE score SET score = ? WHERE ID = ?", (id_A[1]-40 , id_A[0]))
                cursor.execute("UPDATE score SET score = ? WHERE ID = ?", (id_B[1]-40 , id_B[0]))
                connection.commit()

                print("組隊成功")
                print(classes,'A:'+memberA,'B:'+memberB,rA,rB)
                messagebox.showinfo("組隊成功","各扣除40積分")

            else:
                messagebox.showerror("組隊失敗","分數餘額不足，請確認再試")
                print("餘額不足")
                print(classes,'A:'+memberA,'B:'+memberB,rA,rB)
        else:
            messagebox.showerror("組隊失敗","其中有人已在隊伍中")
            print("重複組隊")
            print(classes,'A:'+memberA,'B:'+memberB,ser1,ser2)


def btn_add():#增員
    dbset()
    party = entry_3.get()#組別
    memberA = entry_1.get()
    flagM = False
    flagP = False


    #查成員
    memA = cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (memberA,))
    rA = memA.fetchone()
    if rA != None:
        flagM =True
        print(rA)
    else:
        messagebox.showerror("錯誤","輸入的學號不存在，請檢查")
        print("學號不存在，請檢查錯誤")

    if flagM == True:
        c = cursor.execute("SELECT * FROM team WHERE ID LIKE ?", ('%' + memberA + '%',))
        ser1 = c.fetchone()
        if ser1 != None:
            messagebox.showerror("錯誤","此學號已在隊伍中，請檢查")
            print("此學號已在隊伍中，請檢查錯誤")        
        else:
            
            try: #查組別
                c = cursor.execute("SELECT * FROM team WHERE party = ? ORDER BY party DESC LIMIT 1", (party,))
                p_info = c.fetchone()
                flagP =True
                print(flagP)
            except:
                messagebox.showerror("錯誤","輸入的隊伍不存在，請檢查")
                print("隊伍不存在，請檢查錯誤")

            if flagM == True and flagP == True:
                m_info = p_info[2].split(',')
                memnum = p_info[1]
                score_list = []
                        
                for i in range(int(memnum)):
                    c= cursor.execute("SELECT * FROM score WHERE ID = ? ORDER BY ID DESC LIMIT 1", (m_info[i],))
                    sc = c.fetchone()
                    score_list.append(sc[2])

                score_list.append(rA[2])
                m_info.append(rA[0])
                sc_bonus = (int(memnum)-1) * 5 + 40
                ans_mem = True

                for i in score_list:
                    if int(i) <= sc_bonus:
                        ans = False
                        messagebox.showerror("錯誤","組別成員分數不足")
                        break

                t = ''
                for i in m_info:
                    if i == m_info[len(m_info)-1]:
                        t += str(i)
                    else:
                        t += str(i)+','

                for i in range(len(score_list)):
                    cursor.execute("INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (m_info[i], '組隊扣除積分', '組隊積分扣除 ' + str(sc_bonus), time.strftime("%m-%d %H:%M")))
                    cursor.execute("UPDATE score SET score = ? WHERE ID = ?", (int(score_list[i]) -  sc_bonus ,m_info[i]))
                    connection.commit()

                cursor.execute("UPDATE team SET ID = ?, mem = ? WHERE party = ?", (t , int(p_info[1])+1, party))
                connection.commit()

                print("組隊成功")
                print(t, party)
                print(m_info)
                print(score_list)
                messagebox.showinfo("組隊成功","各扣除" + str(sc_bonus) +"積分")
            else:#再查看分數
                print('有一個不是TRUE')



def btn_merge(): #合併
    dbset()
    boxA = entry_4.get()
    boxB = entry_8.get()
    flag_mer = False
    c = cursor.execute("SELECT * FROM team WHERE party = ? ORDER BY party DESC LIMIT 1", (boxA,))
    boxA = c.fetchone()
    c = cursor.execute("SELECT * FROM team WHERE party = ? ORDER BY party DESC LIMIT 1", (boxB,))
    boxB = c.fetchone()
    flag_mer = True
    if boxA == None or boxB ==None:
        print("組隊輸入問題")
        messagebox.showerror("合併失敗","隊伍序號錯誤")
    else:
        if flag_mer:
            id_A = boxA[2].split(',')
            id_B = boxB[2].split(',')
            mer_list = id_A + id_B
            t = ''
            for i in mer_list:
                if i != mer_list[len(mer_list)-1]:
                    t+= i + ','
                else:
                    t += i
                cursor.execute("INSERT INTO history (ID, action, info, time) VALUES (?, ?, ?, ?)", (i,'隊伍變動','隊伍合併',time.strftime("%m-%d %H:%M")))
            print("修改",t)

            
            cursor.execute("UPDATE team SET mem = ? ,ID = ? WHERE party = ?", (len(mer_list), t, boxA[0]))
            cursor.execute("DELETE FROM team WHERE party = ?", (boxB[0],))


            print(boxA[0], len(mer_list),t)
            print('mer=',mer_list)


def btn_query():#查詢
    dbset()
    box = entry_7.get()
    c = cursor.execute("SELECT * FROM team WHERE party = ? ORDER BY party DESC LIMIT 1", (box,))
    ser1 = c.fetchone()
    id = ser1[2].split(',')
    t = '組別人員為:\n'
    for i in id:
        t += i + '\n'
    canvas.itemconfig(query_ID, text=t)
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
entry_2.insert(0, '109051219')

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
entry_5.insert(0, '109051046')

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
    command=btn_merge,
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
    command=btn_query,
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
    command=btn_add,
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

query_ID = canvas.create_text(
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