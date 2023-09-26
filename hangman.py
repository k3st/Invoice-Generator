print("Welcome To HANGMAN GAME")

def searchWord(lett):
    for i in arrGuess:
        if i == lett:
            arrGuess.remove(i)
            return True

def displayClue(no):
    if (no == 0):
        print("\nThe Game will now START!!!\n\n")
        for i in arrGuess:
            print("__  ", end ="" )
        print("\n\n\n")
        return
    
        

arrGuess=[]
guess = input("Enter a word to guess: ")

for i in guess:
    arrGuess.append(i)
##    print(i, end= ", ")

##print(arrGuess) ##@@
##arrGuess.sort()
displayClue(0)

word = False
while(guess != word):
    oneLet =input("Enter a single letter: ")
    if (searchWord(oneLet) == True):
        print(oneLet + " is Correct")
        print(arrGuess) # checker
    else:
        print("incorrect")
