import random_word


# function for replacing character using the index
def replace_by_index(word, index, chart):
    return word[:index] + chart + word[index+1:]

# create the existent word
wordToGuess = random_word.RandomWords().get_random_word()
letters = [x for x in wordToGuess]

showWord = "_"*len(wordToGuess)
numberOfLives = 8

print("This is console Hangman game. You have 8 lives. In this number of attempts you have to guess the word I gіve you.\n"
      "You have to enter one character at a time. If there is more than one, only the first character will be selected. Good Luck!\n")

print("The word is:\n"
      f"{showWord}")

while numberOfLives > 0:
    # user input
    userEnter = input()

    if userEnter == '':
        userEnter = "^"
    else:
        userEnter = str(userEnter)[0]

    # check if entered letter is in word
    if userEnter in letters:
        indexes = [ind for ind in range(0, len(wordToGuess)) if userEnter == wordToGuess[ind]]
        for i in indexes:
            showWord = replace_by_index(showWord, i, userEnter)

        if "_" in showWord:
            print("The word is:\n"
                  f"{showWord}")
        else:
            print(f"YOU WON! The given word is {wordToGuess}\n"
                  f"{numberOfLives} life left")

    else:
        numberOfLives -= 1

        if numberOfLives == 0:
            print(f"Game OVER! The given word is {wordToGuess}")
            break
        elif numberOfLives == 1:
            print(f"Wrong! {numberOfLives} life left")
        else:
            print(f"Wrong! {numberOfLives} lives left")