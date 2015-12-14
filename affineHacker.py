import detectEnglish
import cryptomath
import affine_cipher
import sys
import os

SILENT_MODE = True


def main():
    if not os.path.exists('cipher_text.txt'):
        sys.exit('cipher_text.txt not exist')

    cipherTextFile = open('cipher_text.txt')
    cipherText = cipherTextFile.read()
    cipherTextFile.close

    plainText = hackAffine(cipherText)

    print('Cipher message: ' + cipherText)
    if plainText is not None:
        print('Decrypted message: ' + plainText)
    else:
        print('Decrypted message: None')


def hackAffine(message):
    print('Hacking...')
    print('(Press Ctrl-C or Ctrl-D to stop at any time)')

    for key in range(len(affine_cipher.SYMBOLS) ** 2):
        keyA = affine_cipher.getKeyParts(key)[0]
        if cryptomath.gcd(keyA, len(affine_cipher.SYMBOLS)) != 1:
            continue

        text = affine_cipher.decryptMessage(key, message)
        if SILENT_MODE is False:
            print()
            print('+: key:\t%s' % (key))
            print('+: msg:\t%s' % (text[200:]))
            print()

        if detectEnglish.isEnglish(text) is True:
            print()
            print('+: key:\t%s' % (key))
            print('+: msg:\t%s' % (text[200:]))
            print()
            print('Enter D for done, or just press Enter to continue')
            prompt = input('> ')
            if prompt.upper().startswith('D') is True:
                return text
    return None


if __name__ == '__main__':
    main()
