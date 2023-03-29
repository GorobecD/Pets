import random


diceSides = list(range(1, 7))

while True:
    userInput = input("Roll dice?\n"
                      "(y) Yes\n"
                      "(n) No\n").lower()

    if userInput == 'y':
        print(random.choice(diceSides))
    else:
        break
