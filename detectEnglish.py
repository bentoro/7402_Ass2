#!/usr/bin/python3.5

# Detect English module
# Provides all of the functions needed to find dictionary words

# returns True or False
# Uses a "dictionary.txt" file in the current directory with English words in it, one word per line.
import math, sys
from sys import argv
UpperCase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Alphabet = UpperCase + UpperCase.lower() + ' \t\n'

def main():
    if len (sys.argv[1:]) < 1:
        print ('Usage: ./trdecode.py file')
        sys.exit(2)
    a, filename = argv
    file = open(filename)

    for key in range (1,len(file.read())):
        print("Trying key #%s "%(key))
        decryptedmsg = decryptMessage(key, file.read())

        if FindEnglish(decryptedmsg):
            print("Possible encryption:")
            print("Key %s: %s " % (key,decryptedmsg))
            response = raw_input("Enter D for done, or press enter to continue:")
            if response.strip().upper().startswith('D'):
                print("Encrypted message:")
                print (decryptedmsg)
                exit()

    return None



def decryptMessage(key, message):
    # Determine the number of columns
    nCols = math.ceil (len (message) / key)
    # Determine the number of rows
    nRows = key
    # Determine the unused cells
    nUnused = (nCols * nRows) - len(message)
    # Each string in plaintext represents a column in the grid.
    plaintext = [''] * int(nCols)
    # row and col point to the location of the next character in the ciphertext
    row = col = 0
    for symbol in message:
        plaintext[col] += symbol
        col += 1 # point to next column
        # If it reaches the last column in the row, or at an unused cell, start processing the next row
        if (col == nCols) or (col == nCols - 1 and row >= nRows - nUnused):
            col = 0
            row += 1
    return ''.join(plaintext)

def loadDictionary():
    dictionaryFile = open ('dictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None   # the very last item is "none" -> no match
    dictionaryFile.close()
    return englishWords


# breaks the string up into individual words and matches them agains the dictionary to find the number of matches
def getWordCount (message):
    WordList = loadDictionary()
    message = message.upper()
    message = removeNonLetters (message)
    possibleWords = message.split()

    if possibleWords == []:
        return 0.0 # no matches found

    matches = 0
    for word in possibleWords:
        if word in WordList:
            matches += 1
    return float (matches) / len (possibleWords)

# Remove all the non-letter characters from the string
def removeNonLetters (message):
    lettersOnly = []
    for symbol in message:
        if symbol in Alphabet:
            lettersOnly.append (symbol)
    return ''.join (lettersOnly)


# Given the thersholds, return true of false for a wordmatch and a letter match
def FindEnglish (message, wordPercentage = 20, letterPercentage = 85):

    wordsMatch = getWordCount (message) * 100 >= wordPercentage
    numLetters = len(removeNonLetters (message))
    messageLettersPercentage = float (numLetters) / len (message) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

if __name__ == '__main__':
    main()
