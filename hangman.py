print("Welcome To HANGMAN GAME")

def searchWord(lett):
    for i in arrGuess:
        if i == lett:
            dictGuess.update({i:True})
            displayClue()
            arrGuess.remove(i)
            return True

def displayClue():
    print("-----"*15)
    print("\n\n")
    for i in dictGuess:
        if(dictGuess.get(i) == True):
            print(i, end =" ")
        else:
            print("__  ", end ="" )
    
    print("\n\n") #spacer
      
    
arrGuess=[]
dictGuess={}
guess = input("Enter a word to guess: ")

for i in guess:
    arrGuess.append(i.upper())
    dictGuess[i.upper()] = False

##print(arrGuess,dictGuess) ##@@ checker
print("\nThe Game will now START!!!\n\n")
displayClue()

word = False
while(guess != word):
    oneLet =input("Enter a single letter: ")
    oneLet = oneLet.upper()
    if (searchWord(oneLet) == True):
        print("\n",oneLet , " is Correct")        
##        print(arrGuess) ##@@  checker
    else:
        print("incorrect")
