import sys, random, cryptomath

# Symbol set
SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

def main():
    message = """A computer would deserve to be called intelligent if it 
could deceive a human into believing that it was human." -Alan Turing"""
    key = getRandomKey()

    mode = 'encrypt'
    translated = encryptMessage(key, message)
    print('Key: %s' % (key))
    print('%sed text:' % (mode.title()))
    print(translated)
    mode = 'decrypt'
    plaintext = decryptMessage(key, translated)
    print(plaintext)

def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''

    for sym in message:
        if sym in SYMBOLS:
            symIndex = SYMBOLS.find(sym)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += sym
    return ciphertext

def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    modInverseOfKeyA = cryptomath.findModInverse(keyA, len(SYMBOLS))
    plaintext = ''

    for sym in message:
        if sym in SYMBOLS:
            symIndex = SYMBOLS.find(sym)
            plaintext += SYMBOLS[((symIndex - keyB) * modInverseOfKeyA) % len(SYMBOLS)]
        else:
            plaintext += sym
    return plaintext

def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)

def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key A is set to 1.')
    if keyB == 0 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key B is set to 0.')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit('Key A must be greater than 0 and key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if cryptomath.gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit('Key A (%s) and symbol set size (%s) are not relatively prime.' % (keyA, len(SYMBOLS)))

def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptomath.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB

if __name__ == '__main__':
    main()
