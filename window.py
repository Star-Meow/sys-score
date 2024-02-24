from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import ttk,Tk, Canvas, Entry, Text, Button, PhotoImage
import time
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\github\sys-score\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def sent_btn():
    nowtime = time.strftime("%m-%d %H:%M")
    entry_contents = [
        entry_class.get(),
        entry_name.get(),
        entry_action.get(),
        entry_info.get(),
        nowtime
    ]
    print("Entry框的內容:")
    for content in entry_contents:
        print(content)


window = Tk()

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
    file=relative_to_assets("entry_4.png"))
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
    file=relative_to_assets("entry_2.png"))
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
    file=relative_to_assets("entry_3.png"))
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
    file=relative_to_assets("entry_1.png"))
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
    file=relative_to_assets("button_1.png"))
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


window.resizable(False, False)
window.mainloop()
