import sys
import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def translateMessage(key, text, mode):
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        charsA, charsB = charsB, charsA
    for c in text:
        if c.upper() in charsA:
            cIndex = charsA.find(c.upper())
            if c.isupper():
                translated += charsB[cIndex]
            else:
                translated += charsB[cIndex].lower()
        else:
            translated += c
    return translated


# This function may not be used, just for in case
def getRandomKey():
    keyList = list(LETTERS)
    random.shuffle(keyList)
    return ''.join(keyList)


def checkValidKey(key):
    letterList = list(LETTERS)
    keyList = list(key)
    letterList.sort()
    keyList.sort()
    if keyList != letterList:
        sys.exit('The key has some problem')


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def main():
    message = """If a man is offered a fact which goes against his
 instincts, he will scrutinize it closely, and unless the evidence is
 overwhelming, he will refuse to believe it. If, on the other hand, he is
 offered something which affords a reason for acting in accordance to his
 instincts, he will accept it even on the slightest evidence. The origin of
 myths is explained in this way. -Bertrand Russell"""
    # key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    key = getRandomKey()
    mode = 'encrypt'
    checkValidKey(key)

    print("original:")
    print(message)

    if mode == 'encrypt':
        translatedMessage = encryptMessage(key, message)
        print('key: %s' % (key))
        print('cipher: %s' % (translatedMessage))
    elif mode == 'decrypt':
        translatedMessage = decryptMessage(key, message)
        print('key: %s' % (key))
        print('clear: %s' % (translatedMessage))


if __name__ == '__main__':
    main()
