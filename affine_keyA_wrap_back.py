import affine_cipher, cryptomath

for keyA in range(2, 100):
    key = keyA * len(affine_cipher.SYMBOLS) + 1
    if cryptomath.gcd(keyA, len(affine_cipher.SYMBOLS)) == 1:
        print(keyA, affine_cipher.encryptMessage(key, "simple, not simpler"))

