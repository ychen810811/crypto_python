import sys
import os
import pprint


def makeWordPattern(word):
    word = word.upper()
    num = 0
    letterMap = {}
    pattern = []
    for char in word:
        if char not in letterMap:
            letterMap[char] = num
            num += 1
        pattern.append(str(letterMap[char]))
    return '.'.join(pattern)


def main():
    allPatterns = {}

    fo = open('dict.txt')
    wordList = fo.read().split('\n')
    fo.close()

    # allPatterns[wordList[0]] = ['helloworld']

    for word in wordList:
        pattern = makeWordPattern(word)
        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    if os.path.exists('wordPatterns.py'):
        print('Overwite existing file? (y/n)')
        response = input('>> ')
        if response.lower().startswith('n'):
            sys.exit('Abort execution')
        else:
            print('You have decided to continue with \'%s\'' % (response))
    fo = open('wordPatterns.py', 'w')
    fo.write('allPatterns = ')
    fo.write(pprint.pformat(allPatterns))
    fo.close()

if __name__ == '__main__':
    main()
