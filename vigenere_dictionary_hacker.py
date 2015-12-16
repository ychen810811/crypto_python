import vigenere_cipher
import detectEnglish


def hack(message):
    fo = open('dict.txt')
    words = fo.readlines()
    fo.close()
    for word in words:
        word = word.strip()
        decrypted = vigenere_cipher.decrypt(message, word)
        if detectEnglish.isEnglish(decrypted, wordPercentage=40.0):
            print()
            print('Possible encryption break:')
            print('Key ' + str(word) + ':' + decrypted[:100])
            print()
            print('Enter D for done, or just press Enter to continue breaking:')
            response = input('> ')
            if response.lower().startswith('d'):
                return decrypted
    return None


def main():
    message = """Tzx isnz eccjxkg nfq lol mys bbqq I lxcz."""
    hacked = hack(message)
    if hacked is not None:
        print(hacked)
    else:
        print('Fail to hack the message with Dictionary Method')


if __name__ == '__main__':
    main()