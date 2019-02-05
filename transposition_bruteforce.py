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
import math, sys, argparse, trdecode, trencode, detectEnglish
from sys import argv

def main(argv):

    filename = ""
    message = ""
    content = ""

    if len (sys.argv[1:]) < 2:
        print ('Usage: ./transposition_bruteforce.py -f <ciphertext file> or -m <ciphertext message>')
        sys.exit(2)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action="store",dest="filename")
    parser.add_argument('-m', action="store",dest="message")

    print(parser.parse_args().filename)
    print(parser.parse_args().message)
    filename = str(parser.parse_args().filename)

    if parser.parse_args().filename:
        file = open(filename)
        content = file.read()
    else:
        file = open('input.txt', 'w+')
        file.write(parser.parse_args().message)
        file = open('input.txt', 'r')
        content = file.read()

    for key in range (1,len(content)):
        print("Trying key #%s "%(key))
        decryptedmsg = trdecode.decryptMessage(key, content)

        if detectEnglish.FindEnglish(decryptedmsg):
            print("Possible encryption:")
            print("Key %s: %s " % (key,decryptedmsg))
            response = raw_input("Enter y if done, or press enter to continue:")
            if response.strip().lower().startswith('y'):
                print("Encrypted message:")
                print (decryptedmsg)
                exit()
    return None

if __name__ == '__main__':
    main(sys.argv[1:])
