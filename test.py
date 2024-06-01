import datetime,time


date = "01/01"
nowtime = time.strftime("%m/%d")


date1 = time.strptime(nowtime, "%m/%d")
date2 = time.strptime(date, "%m/%d")

print(date1)
print(date2)

if date1 > date2:
    print("YES")
else:
    print("NO")

