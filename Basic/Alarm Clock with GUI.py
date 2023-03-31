from datetime import datetime
import time
import tkinter as tk
import beepmusic


def increase(obj, isHour):
    num = int(obj.cget("text")) + 1
    obj["text"] = num % 24 if isHour else num % 60

    check_format(obj)


def decrease(obj, isHour):
    num = int(obj.cget("text")) - 1
    obj["text"] = num % 24 if isHour else num % 60

    check_format(obj)


def check_format(label):
    num = str(label.cget("text"))
    if len(num) == 1:
        label["text"] = "0" + num


def set_alarm():
    aimHours = int(hoursLB.cget("text"))
    aimMinutes = int(minutesLB.cget("text"))
    aimSeconds = int(secondsLB.cget("text"))

    while True:
        today = datetime.now()

        if today.hour == aimHours and today.minute == aimMinutes and today.second == aimSeconds:
            break

        root.after(500)
        beepmusic.beepmusic.Beep(300, 200)
    beepmusic.beepmusic.Beep(1000, 2000)


root = tk.Tk()

hoursUpBT = tk.Button(root, text="↑", font=('Times', 24), width=6)
minutesUpBT = tk.Button(root, text="↑", font=('Times', 24), width=6)
secondsUpBT = tk.Button(root, text="↑", font=('Times', 24), width=6)

hoursUpBT.grid(column=0, row=0, sticky='nesw')
minutesUpBT.grid(column=1, row=0, sticky='nesw')
secondsUpBT.grid(column=2, row=0, sticky='nesw')

hoursLB = tk.Label(root, text='00', borderwidth=3, relief='solid', font=('Times', 30), height=2)
minutesLB = tk.Label(root, text='00', borderwidth=3, relief='solid', font=('Times', 30))
secondsLB = tk.Label(root, text='00', borderwidth=3, relief='solid', font=('Times', 30))

hoursUpBT['command'] = lambda: increase(hoursLB, True)
minutesUpBT['command'] = lambda: increase(minutesLB, False)
secondsUpBT['command'] = lambda: increase(secondsLB, False)

hoursLB.grid(column=0, row=1, sticky='nesw')
minutesLB.grid(column=1, row=1, sticky='nesw')
secondsLB.grid(column=2, row=1, sticky='nesw')

hoursDownBT = tk.Button(root, text="↓", font=('Times', 24))
minutesDownBT = tk.Button(root, text="↓", font=('Times', 24))
secondsDownBT = tk.Button(root, text="↓", font=('Times', 24))

hoursDownBT['command'] = lambda: decrease(hoursLB, True)
minutesDownBT['command'] = lambda: decrease(minutesLB, False)
secondsDownBT['command'] = lambda: decrease(secondsLB, False)

hoursDownBT.grid(column=0, row=2, sticky='nesw')
minutesDownBT.grid(column=1, row=2, sticky='nesw')
secondsDownBT.grid(column=2, row=2, sticky='nesw')

setAlarmBT = tk.Button(root, text="Set Alarm", borderwidth=2, relief='solid', height=1, font=('Times', 24), command=set_alarm)
setAlarmBT.grid(column=0, row=3, columnspan=3, sticky='nesw')

root.mainloop()
