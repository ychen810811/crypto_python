# -*- coding:utf-8 -*-
# This module provides a RSA cipher "textbook" implementation

import os
import sys
import random
import cryptomath

DEBUG_LEVEL = 1

DEFAULT_BLK_SIZE = 128  # default dealing with blocks of 128 bytes (1024 bits)
BYTE_MAX_INT = 256  # maximum int for a unsigned byte


# Returns a pub/private key pair with keys of _size_ bits in length
# The key pair are returned as a tuple object as below, in which pub key is
# _n_ and _e_ while private key is _n_ and _d_.
#   key pair tuple: ((n, e), (n, d))
def keypair(size=1024):
    # Step 1: generate 2 large primes p and q, calculate n = p * q
    p, q = cryptomath.largeprime(size), cryptomath.largeprime(size)
    n = p * q
    if DEBUG_LEVEL > 0:
        print('p = %s' % p)
        print('q = %s' % q)
        print('n = %s' % n)
    # Step 2: generate a random e which is relatively prime with
    # (p - 1) * (q - 1)
    t = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2 ** (size - 1), 2 ** size)
        if cryptomath.gcd(e, t) == 1:
            break
    if DEBUG_LEVEL > 0:
        print('t = %s' % t)
        print('e = %s' % e)
    # Step 3: calculate d which is the mod inverse of e
    d = cryptomath.findModInverse(e, t)
    if DEBUG_LEVEL > 0:
        print('d = %s' % d)
    pub = (n, e)
    pri = (n, d)
    if DEBUG_LEVEL > 0:
        print('Pub: ', pub)
        print('Pri: ', pri)
    # Return the key pair
    return (pub, pri)


# Create a key pair of keys of _size_ in length and store the public key into
# _filename_pubkey.txt_ and the private key into _filename_privkey.txt_
def storekey(filename, size=1024):
    # We never overwrite existing key files
    if os.path.exists('%s_pubkey.txt' % filename) or os.path.exists('%s_privkey.txt'):
        sys.exit('WARNING: %s_pubkey.txt or %s_privkey.txt already exists. Use a different filename or delete the file(s) and rerun' % (filename, filename))

    file_pri = open('%s_privkey.txt' % filename, 'w')
    pubkey, prikey = keypair(size)
    print()
    print('The public key is a %s and %s digit number.' % (len(str(pubkey[0])), len(str(pubkey[1]))))
    print('Writing the public key into file %s_pubkey.txt...' % filename)
    file_pub = open('%s_pubkey.txt' % filename, 'w')
    file_pub.write('%s,%s,%s' % (size, pubkey[0], pubkey[1]))
    file_pub.close()
    print()
    print('The private key is a %s and %s digit number.' % (len(str(prikey[0])), len(str(prikey[1]))))
    print('Writing the private key into file %s_privkey.txt...' % filename)
    file_pri = open('%s_privkey.txt' % filename, 'w')
    file_pri.write('%s,%s,%s' % (size, prikey[0], prikey[1]))
    file_pri.close()


# Load a key pair from _keyfile_ and return the _key_size, _n_ and _e_or_d_ as a tuple
def loadkey(keyfile):
    fo = open(keyfile)
    content = fo.read()
    fo.close()
    size, n, e_or_d = content.split(',')
    return (int(size), int(n), int(e_or_d))


# Internal function: covert the _message_ string value into a list of integers,
# each integer represents _blk_size_ bytes of string characters
def _blocks_from_message(message, blk_size=DEFAULT_BLK_SIZE):
    msg_bytes = message.encode('ascii')
    blks = []
    for blk_start in range(0, len(msg_bytes), blk_size):
        integer = 0
        for i in range(blk_start, min(blk_start + blk_size, len(msg_bytes))):
            integer += msg_bytes[i] * (BYTE_MAX_INT ** (i % blk_size))
        blks.append(integer)
    return blks


# Internal function: covert a list of integers _blks_ back to a string format
def _message_from_blocks(blks, msg_len, blk_size=DEFAULT_BLK_SIZE):
    msg = []

    for integer in blks:
        sub_msg = []
        for i in range(min(blk_size, msg_len) - 1, -1, -1):
            ascii_code = integer // (BYTE_MAX_INT ** i)
            sub_msg.insert(0, chr(ascii_code))
            integer %= BYTE_MAX_INT ** i
        msg.extend(sub_msg)
        msg_len -= DEFAULT_BLK_SIZE
    return ''.join(msg)


# Encrypt a _message_ with pubkey _key_, and return the encrypted blocks
def encrypt(message, key, blk_size=DEFAULT_BLK_SIZE):
    n, e = key
    blks = _blocks_from_message(message, blk_size)
    encrypted_blks = []
    for blk in blks:
        # RSA algo: ciphertext = plaintext ^ e % n
        encrypted_blks.append(pow(blk, e, n))
    return encrypted_blks


# Decrypt a list of _blks_ with private _key_, and return the decrypted message
def decrypt(blks, key, msg_len, blk_size=DEFAULT_BLK_SIZE):
    decrypted_blks = []
    n, d = key
    for blk in blks:
        # RSA algo: plaintext = ciphertext ^ d % n
        decrypted_blks.append(pow(blk, d, n))
    return _message_from_blocks(decrypted_blks, msg_len, blk_size)


# Encrypt _message_ with private key stored in _keyfile_, and save the ecrypted
# blocks into file _output_. The ecrypted blocks (in string format) are also
# returned
def encrypt_and_save(message, keyfile, output, blk_size=DEFAULT_BLK_SIZE):
    key_size, n, e = loadkey(keyfile)
    if key_size < blk_size * 8:
        sys.exit('Error: key size smaller than block size!')
    encrypted_blks = encrypt(message, (n, e), blk_size)
    for i in range(len(encrypted_blks)):
        encrypted_blks[i] = str(encrypted_blks[i])
    encrypted_content = ','.join(encrypted_blks)
    encrypted_content = '%s_%s_%s' % (len(message), blk_size, encrypted_content)
    fo = open(output, 'w')
    fo.write(encrypted_content)
    fo.close()
    return encrypted_content


# Read from the file _cipherfile_ the encrypted blocks, decrypt them with the
# pubic key stored in _keyfile_, and return the decrypted message
def read_and_decrypt(cipherfile, keyfile):
    key_size, n, d = loadkey(keyfile)
    fo = open(cipherfile)
    msg_len, blk_size, content = fo.read().split('_')
    msg_len = int(msg_len)
    blk_size = int(blk_size)
    fo.close()
    if key_size < blk_size:
        sys.exit('Error: key size smaller than block size!')
    blks = []
    for blk in content.split(','):
        blks.append(int(blk))
    return decrypt(blks, (n, d), msg_len, blk_size)


def main():
    message = """"Journalists belong in the gutter because that is
where the ruling classes throw their guilty secrets." -Gerald Priestl and "The
Founding Fathers gave the free press the protection it must have to bare the
secrets of government and inform the people." -Hugo Black"""
    encrypted = encrypt_and_save(message, 'tmp_pubkey.txt', 'tmp_encrypted.txt', 128)
    print('\n\nEncrypted:')
    print(encrypted)

    decrypted = read_and_decrypt('tmp_encrypted.txt', 'tmp_privkey.txt')
    print('\n\nDecrypted:')
    print(decrypted)


if __name__ == '__main__':
    main()
