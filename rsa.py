# -*- coding:utf-8 -*-
# This module provides a RSA cipher "textbook" implementation

import os
import sys
import random
import cryptomath

DEBUG_LEVEL = 1


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
# filename_pubkey.txt and the private key into filename_privkey.txt
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


def main():
    storekey('tmp', 1024)


if __name__ == '__main__':
    main()