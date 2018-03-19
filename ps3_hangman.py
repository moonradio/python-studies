# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random

WORDLIST_FILENAME = "words.txt"
STATS_FILENAME = "stats2.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def loadStats():
    """
    Returns number of played games, games won by user, average number of tries.
    """
    print("Loading stats from file...")
    # inFile: file
    inFile = open(STATS_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # statslist: list of ints
    statslist = line.split()
    statslistInt = []
    for item in statslist:
        statslistInt += [float(item),]
    return statslistInt

def writeStats(statslistInt):
    """
    Writes updated stats in the stats file.
    """
    print("Writing stats to file... OK!")
    inFile = open(STATS_FILENAME, 'w')
    inFile.seek(0)
    inFile.truncate()
    statsLine = ''
    for item in statslistInt:
        statsLine = statsLine + " " + str(item)
    inFile.write(statsLine)       
    return

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    isGuessed = True
    for letter in secretWord:
        if letter in lettersGuessed:
            isGuessed = True
        else:
            isGuessed = False
            break
    return isGuessed

def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    userWord = ''
    for letter in secretWord:
        if letter in lettersGuessed:
            userWord += letter
        else:
            userWord += '_ '
    return userWord

def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    import string
    availableLetters = ''
    for letter in string.ascii_lowercase:
        if letter not in lettersGuessed:
            availableLetters +=letter
    return availableLetters

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    lettersGuessed = []
    mistakesMade = 0
    statslistInt = loadStats()
    print("Welcome to the game, Hangman!")
    print("***Some stats here:")
    print("***Total games played: "+str(int(statslistInt[0])))
    print("***Total games won by user: "+str(int(statslistInt[1])))
    print("***That makes "+str("{:4.2f}".format((statslistInt[1]/statslistInt[0])*100))+"% of games won by user!")
    print("***Average tries used to guess the word: "+str(statslistInt[2]))
    print("I am thinking of a word that is "+str(len(secretWord))+" letters long.")
    
    while mistakesMade < 8:
        availableLetters = getAvailableLetters(lettersGuessed)
        print("-----------")
        print("You have "+str(8 - mistakesMade)+" guesses left.")
        print("Available Letters: "+str(availableLetters))  
        guess = str(input("Please guess a letter: "))
        guessInLowerCase = guess.lower()
        if guessInLowerCase in lettersGuessed:
            print("Oops! You've already guessed that letter: "+str(getGuessedWord(secretWord, lettersGuessed))) 
        elif guessInLowerCase in secretWord:
            lettersGuessed += guessInLowerCase
            print("Good guess: "+str(getGuessedWord(secretWord, lettersGuessed)))
            if isWordGuessed(secretWord, lettersGuessed) == True:
                print("-----------")
                print("Congratulations, you won!")
                statslistInt[1] += 1
                break
        else:
            lettersGuessed += guessInLowerCase
            print("Oops! That letter is not in my word: "+str(getGuessedWord(secretWord, lettersGuessed)))
            mistakesMade += 1
            if mistakesMade == 8:
                print("-----------")
                print("Sorry, you ran out of guesses. The word was "+str(secretWord)+".") 
    avg = ((statslistInt[2]*statslistInt[0]+mistakesMade+1)/(statslistInt[0]+1))
    statslistInt[2] = round(avg, 2)
    statslistInt[0] += 1
    writeStats(statslistInt)
    return  

# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secretWord while you're testing)

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
