import tkinter as tk
import MainWindow as mv
import time


def play():
    global canvas
    circle_data = mv.circle_data

    cycle(circle_data)


def cycle(circle_data):
    circle_data.gen_coordinates(900, 700)
    print(circle_data.get_coordinates())

    target = canvas.create_oval(circle_data.get_coordinates()[0] - circle_data.get_radius(),
                                circle_data.get_coordinates()[1] - circle_data.get_radius(),
                                circle_data.get_coordinates()[0] + circle_data.get_radius(),
                                circle_data.get_coordinates()[1] + circle_data.get_radius())

    canvas.after(circle_data.get_vanish_time() * 1000, cycle(circle_data))
    canvas.delete(target)


root = tk.Tk()
root.title('Target Practice Game')
root.geometry('900x700')

canvas = tk.Canvas(root, width=900, height=700)
canvas.pack()

play()

root.mainloop()