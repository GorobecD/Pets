from gtts import gTTS
import os


userText = input("Enter the text you need to convert into speech: ")
language = 'en'

userSpeach = gTTS(text=userText, lang=language, slow=False)

userSpeach.save('welcome.mp3')
os.system('welcome.mp3')