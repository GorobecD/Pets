# Main menu (Infinite mode, Time mode, difficult selecting)
# Draws a circle different sizes depending on the level difficult
# User clicks on the circle, and it's disappear
#

import Target
import tkinter as tk


def start():
    global circle_data
    var_val = 4 - int(varDiff.get())
    radius = 10 * var_val
    vanish = var_val

    circle_data = Target.CircleTarget(radius, vanish)

    root.destroy()
    import PracticeWindow


circle_data = None

root = tk.Tk()
root.title('Target Practice Game')
root.geometry('900x700')

varDiff = tk.IntVar()

startButton = tk.Button(root, text='Start', width=10, command=start)
startButton.pack()

diffLabel = tk.Label(root, text='Difficult:')
diffLabel.pack(pady=(20, 0))

diffEasyRB = tk.Radiobutton(root, text='Easy', value=1, variable=varDiff)
diffEasyRB.select()
diffEasyRB.pack()

diffNormalRB = tk.Radiobutton(root, text='Normal', value=2, variable=varDiff)
diffNormalRB.pack()

diffHardRB = tk.Radiobutton(root, text='Hard', value=3, variable=varDiff)
diffHardRB.pack()


root.mainloop()



