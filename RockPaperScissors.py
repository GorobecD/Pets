import random


gestures = ["Rock", "Paper", "Scissors"]
botScore = 0
playerScore = 0

while True:
    botChoice = gestures.index(random.choice(gestures)) + 1

    playerChoice = int(input('Choose your gesture:\n'
                           '(1) Rock\n'
                           '(2) Paper\n'
                           '(3) Scissors\n'
                           '(9) Exit\n\n'))

    print(f"\nBot's raised the {gestures[botChoice-1]}\n")

    if abs(playerChoice - botChoice) == 0:
        print("DRAW")
    elif abs(playerChoice - botChoice) == 2:
        if playerChoice < botChoice:
            playerScore += 1
        else:
            botScore += 1
    elif abs(playerChoice - botChoice) == 1:
        if playerChoice > botChoice:
            playerScore += 1
        else:
            botScore += 1
    else:
        if botScore > playerScore:
            print("Bot is a winner!!")
        elif botScore < playerScore:
            print("Player is a winner!!")
        else:
            print("DRAW match!! It's unfair")
        break

    print("The score:\n"
          f"P: {playerScore} -- {botScore} :B")