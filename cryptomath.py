# -*- coding:utf-8 -*-
# Description: This module contains some useful functions in crypto maths
# gcd(a, b)             - Greatest Common Devisor of a and b
# findModInverse(a, m)  - Calculate the a's reverse mod m
# isprime(a)            - Test a integer prime or not
# sieveprime(size)      - Generate a list of primes with Eratosthenes sieve of
#                         size

import math
import pprint


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q*v1), (u2 - q*v2), (u3 - q*v3), v1, v2, v3
    return u1 % m


# Return True is a is prime, False otherwise
def isprime(a):
    if a < 2:
        return False
    for i in range(2, int(math.sqrt(a)) + 1):
        if a % i == 0:
            return False
    return True


# Return a list of prime numbers with the Eratosthenes sieve of the size
def sieveprime(size):
    sieve = [True] * size
    sieve[0], sieve[1] = False, False
    for i in range(2, int(math.sqrt(size)) + 1):
        ptr = i * 2
        while ptr < size:
            sieve[ptr] = False
            ptr += i

    p = []
    for i in range(size):
        if sieve[i]:
            p.append(i)
    return p


if __name__ == '__main__':
    print('This is a cryptographic math library')

    # Testing code
    pprint.pprint(sieveprime(10000))
