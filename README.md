python 3.11 <br>
numpy-1.26.4<br>
pandas-2.2.1 <br>
db-sqlite3 3-0.0.1 <br>

1.使用時 在資料夾內shift+右鍵 -> 用powersell開啟 
![alt text](image.png)<br>
    輸入 python window.py執行
2.輸入學號,課程,分數異動,以及備註(分數目前只接受加減乘除)<br>
>    logic2A資料庫內 有測試用資料 
>    學號       姓名    分數
>    109021071  測試用  100 

3.檢查資料內容請點開
    DB Browser for SQLite資料夾  ->  DB Browser for SQLite.exe
![alt text](image-4.png)<br>
3.選擇資料庫<br>
左方按鍵 打開資料庫<br>
    選擇課程的資料庫 (遊戲邏輯 -> logic  互動媒體 -> media) 
    EX: "media2A.db"為互動媒體2A資料庫 
![alt text](image-2.png)<br>
點選下方Browse Data<br>
![alt text](image-1.png)<br>
    點選下拉式選單<br>
![alt text](image-5.png)<br>
5.資料表查看<br>
score -> 學號 姓名 分數<br>
history -> 學號 更新內容 備註 當下時間
