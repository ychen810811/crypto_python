import sys, os

CAP_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACES = CAP_LETTERS + CAP_LETTERS.lower() + ' \t\n'

def loadDictFile(path = 'dict.txt'):
    if not os.path.exists(path):
        sys.exit('Dictionary file not found')

    dictFile = open(path)
    contents = dictFile.read()
    dictFile.close()

    dictWordList = {}   
    for word in contents.split():
        dictWordList[word] = None
    return dictWordList

ENGLISH_WORDS = loadDictFile('dict.txt')

def removeNonLetters(text):
    t = []
    for c in text:
        if c in LETTERS_AND_SPACES:
            t.append(c)
    return ''.join(t)

def calcEnglishWordPercentage(text):
    text = removeNonLetters(text).upper()
    pieces = text.split()
    numPieces = len(pieces)
    if numPieces == 0:
        return 0.0

    matchCount = 0
    for piece in pieces:
        if piece in ENGLISH_WORDS:
            matchCount += 1
    return (float(matchCount) / numPieces) * 100.0

def calcLetterPercentage(text):
    if len(text) == 0:
        return 0.0

    return (float(len(removeNonLetters(text))) / len(text)) * 100.0

def isEnglish(text, wordPercentage = 20.0, letterPercentage = 85.0):
    wordsMatch = calcEnglishWordPercentage(text) >= wordPercentage
    lettersMatch = calcLetterPercentage(text) >= letterPercentage
    return wordsMatch and lettersMatch

if __name__ == '__main__':
    print('This is a library to test English text')
