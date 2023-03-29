import tkinter as tk
import base64


def enc():
    textForUser['text'] = 'Enter the message to encode:'
    submitButton['text'] = 'Encode'


def dec():
    textForUser['text'] = 'Enter the message to decode:'
    submitButton['text'] = 'Decode'


def submit():
    user_choice = int(var.get())
    user_entry = bytes(entryField.get(), 'UTF-8')

    if user_choice == 1:
        changed_message = base64.encodebytes(user_entry)
    else:
        changed_message = base64.decodebytes(user_entry)

    codedMessage['text'] = str(changed_message, 'UTF-8')


root = tk.Tk()
root.title('Encoder and Decoder')
root.geometry('400x300')


var = tk.IntVar()

textForUser = tk.Label(root, text='Enter the message to encode:')
entryField = tk.Entry(root)

radioButtonEncode = tk.Radiobutton(root, text='Encode', value=1, variable=var, command=enc)
radioButtonEncode.select()

radioButtonDecode = tk.Radiobutton(root, text='Decode', value=2, variable=var, command=dec)

submitButton = tk.Button(root, text="Encode", command=submit)
codedMessage = tk.Label(root)

textForUser.pack()
entryField.pack()
radioButtonEncode.pack()
radioButtonDecode.pack()
submitButton.pack()
codedMessage.pack()

tk.mainloop()
