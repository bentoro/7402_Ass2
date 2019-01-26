#!/usr/bin/python3.5
#
# =====================================================================================
#
#       Filename:  transposition_bruteforce.py
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#        Created:  02/7/2019
#
#         Author:  Benedict Lo
#
# =====================================================================================
import math, sys
from sys import argv
UpperCase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Alphabet = UpperCase + UpperCase.lower() + ' \t\n'


# =====================================================================================
#
#       Function: main
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Benedict Lo
#
#     parameters: none
#
# =====================================================================================
def main():
    if len (sys.argv[1:]) < 1:
        print ('Usage: ./transposition_bruteforce.py file')
        sys.exit(2)
    a, filename = argv
    file = open(filename)
    content = file.read()
    for key in range (1,len(content)):
        print("Trying key #%s "%(key))
        decryptedmsg = decryptMessage(key, content)

        if FindEnglish(decryptedmsg):
            print("Possible encryption:")
            print("Key %s: %s " % (key,decryptedmsg))
            response = raw_input("Enter y if done, or press enter to continue:")
            if response.strip().startswith('y'):
                print("Encrypted message:")
                print (decryptedmsg)
                exit()
    return None


# =====================================================================================
#
#       Function: decryptMessage(key, message)
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Aman Abdulla
#
#     parameters: key - key for the transposition ciphertext
#                 message - ciphertext
#
# =====================================================================================
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

# =====================================================================================
#
#       Function: loadDictionary
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Aman Abdulla
#
#     parameters: none
#
# =====================================================================================
def loadDictionary():
    dictionaryFile = open ('dictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None   # the very last item is "none" -> no match
    dictionaryFile.close()
    return englishWords

# =====================================================================================
#
#       Function: getWordCount(message)
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Aman Abdulla
#
#     parameters: message - ciphertext
#
# =====================================================================================
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

# =====================================================================================
#
#       Function: removeNonLetters(message)
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Aman Abdulla
#
#     parameters: message - ciphertext
#
# =====================================================================================
# Remove all the non-letter characters from the string
def removeNonLetters (message):
    lettersOnly = []
    for symbol in message:
        if symbol in Alphabet:
            lettersOnly.append (symbol)
    return ''.join (lettersOnly)

# =====================================================================================
#
#       Function: FindEnglish(message, wordPercentage, letterPercentage)
#
#    Description: Take file as input and attempts to bruteforce the ciphertext
#
#         Author:  Aman Abdulla
#
#     parameters: message - ciphertext
#
# =====================================================================================
# Given the thersholds, return true of false for a wordmatch and a letter match
def FindEnglish (message, wordPercentage = 20, letterPercentage = 85):

    wordsMatch = getWordCount (message) * 100 >= wordPercentage
    numLetters = len(removeNonLetters (message))
    messageLettersPercentage = float (numLetters) / len (message) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

if __name__ == '__main__':
    main()
