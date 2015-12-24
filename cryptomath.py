# -*- coding:utf-8 -*-
# Description: This module contains some useful functions in crypto maths
# gcd(a, b)             - Greatest Common Devisor of a and b
# findModInverse(a, m)  - Calculate the a's reverse mod m
# isprime(a)            - Test a integer prime or not
# sieveprime(size)      - Generate a list of primes with Eratosthenes sieve of
#                         size

import math
import random
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


# Return True if a is prime, False otherwise
# Note: This function is too slow to check large numbers
def _isprime(a):
    if a < 2:
        return False
    for i in range(2, int(math.sqrt(a)) + 1):
        if a % i == 0:
            return False
    return True


# Returns True if num is a prime number.
def _rabin_miller_test(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s until it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5):  # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


# Return True if num is prime, False otherwise
def isprime(num):
    if num < 2:  # number < 2 are never prime
        return False
    elif num < 1000 * 1000:  # for numbers within [2, 1000000) check with small primes
        small_primes = [2,   3,   5,   7,   11,  13,  17,  19,  23,  29,  31,
                        37,  41,  43,  47,  53,  59,  61,  67,  71,  73,  79,
                        83,  89,  97,  101, 103, 107, 109, 113, 127, 131, 137,
                        139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
                        197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                        263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                        331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
                        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457,
                        461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523,
                        541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
                        607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661,
                        673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
                        751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823,
                        827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
                        907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
                        983, 991, 997]
        if num in small_primes:
            return True
        for p in small_primes:
            if num % p == 0:
                return False
        return True
    else:  # do Rabin Miller test for larger numbers (>= 1000000)
        return _rabin_miller_test(num)


# Return a list of prime with the Eratosthenes sieve of the size
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
    print(isprime(100000096))