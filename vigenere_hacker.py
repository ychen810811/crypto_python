# -*- coding:utf-8 -*-
# Description: a hacker of the Vigenere Cipher based on frequency analysis
# Date of creation: Dec 23 2015

import re
import pprint
import math
import itertools

import vigenere_cipher
import freq_analysis
import detectEnglish

# Debug levels:
#    0  - Debug message off
#    1  - Print basic level of debug messages
# >= 2  - Print verbose debug messages
DEBUG = 1

LETTERS = vigenere_cipher.LETTERS
REGEX_NON_LETTERS = re.compile('[^A-Z]')

MAX_KEY_LEN = 16
NUM_HIGH_FREQ_MATCH_KEYS = 4  # will only consider this number of the most likely subkey candidates


# Return a list of possible key lengths for given cipher text argument. The key
# lengths are a list of integers which are decending ordered.
def _kasiski_examine(cipher_text):
    # Step 1: get the repeated seq spacings.
    repeated_seq_spacings = _repeated_seq_spacing(cipher_text)

    # Step 2: find the most common factors of all the spacings
    # Step 2.1: find the useful factors of each seq
    seq_spacing_factors = {}
    for seq in repeated_seq_spacings:
        if seq not in seq_spacing_factors:
            seq_spacing_factors[seq] = []
        for spacing in repeated_seq_spacings[seq]:
            seq_spacing_factors[seq].extend(_useful_factors(_factors(spacing)))
    if DEBUG > 1:
        pprint.pprint(seq_spacing_factors)

    # Step 2.2: get a list of tuples composed of factors and their occurrences
    factor_count = _common_factors(seq_spacing_factors)
    if DEBUG > 1:
        pprint.pprint(factor_count)

    # Step 3: return the list of possible key lens
    likely_key_len = []
    for t in factor_count:
        likely_key_len.append(t[0])
    if DEBUG > 1:
        pprint.pprint(likely_key_len)
    return likely_key_len


# Find repeated letter sequences thru the message and return a dict value with
# keys of the seq's and values of lists of the spacings.
def _repeated_seq_spacing(message):
    message = REGEX_NON_LETTERS.sub('', message.upper())
    seq_spacing = {}
    for len_seq in range(3, 6):
        for i in range(len(message) - len_seq):
            seq = message[i:i + len_seq]
            for j in range(i + len_seq, len(message) - len_seq):
                if seq == message[j:j + len_seq]:
                    if seq not in seq_spacing:
                        seq_spacing[seq] = [j - i]
                    else:
                        seq_spacing[seq].append(j - i)
    if DEBUG > 1:
        pprint.pprint(seq_spacing)
    return seq_spacing


def _factors(number):
    f = []
    for n in range(1, round(math.sqrt(number)) + 1):
        if number % n == 0:
            f.append(n)
            f.append(number // n)
    f = list(set(f))
    f.sort()
    return f


# Returns a more straightforward list but with double time complexity of the above
def _factors_1(number):
    f = []
    for n in range(1, number + 1):
        if number % n == 0:
            f.append(n)
    return f


def _useful_factors(factors):
    factors = list(set(factors))
    factors.sort()
    if factors == []:
        return []

    if factors[-1] < 2 or factors[0] > MAX_KEY_LEN:
        return []

    i, j = 0, 0
    while factors[i] < 2:  # factors < 2 (1 actually) are usually too little to be a valid factor
        i += 1
    while factors[len(factors) - j - 1] > MAX_KEY_LEN:
        j += 1
    return factors[i:len(factors) - j]


def _common_factors(factors):
    factor_count = {}
    # Step 1: make a dict value of keys of all factors and of values of corresponding repeating count
    for seq in factors:
        for factor in factors[seq]:
            if factor not in factor_count:
                factor_count[factor] = 1
            else:
                factor_count[factor] += 1

    # Step 2: convert the dict value to a list of key-value tuples by the repeating count.
    factor_count = list(factor_count.items())
    factor_count.sort(key=_tuple_2nd_element, reverse=True)
    return factor_count


def _tuple_1st_element(t):
    return t[0]


def _tuple_2nd_element(t):
    return t[1]


def _vigenere_sub_string(nth, key_len, cipher_text):
    cipher_text = REGEX_NON_LETTERS.sub('', cipher_text.upper())
    s = []
    for i in range(len(cipher_text)):
        if i % key_len == nth:
            s.append(cipher_text[i])
    return ''.join(s)


# Returns:
#   None     - if fail to hack the cipher text with the given key length
#   Message  - string containing the hacked message
def _attack_with_key_len(key_len, cipher_text):
    # Try to get the possible letters for each of the subkeys
    # Generate a list of lists of tuples
    subkeys = []
    for i in range(key_len):
        freq_scores = []
        sub_string = _vigenere_sub_string(i, key_len, cipher_text)
        if DEBUG > 0:
            print('sub_key: #%s of %s, sub_string: %s, key candidates:' % (i, key_len, sub_string[:40]))
        for c in LETTERS:
            freq_scores.append((c, freq_analysis.freq_match_score(vigenere_cipher.decrypt(sub_string, c))))
        freq_scores.sort(key=_tuple_2nd_element, reverse=True)
        if DEBUG > 0:
            pprint.pprint(freq_scores)
        subkeys.append(freq_scores[:NUM_HIGH_FREQ_MATCH_KEYS])
    if DEBUG > 0:
        for i in range(key_len):
            print('Possible letters for letter %s of the key: ' % i, end='')
            for t in subkeys[i]:
                print('%s ' % t[0], end='')
            print()
        if DEBUG > 1:
            pprint.pprint(subkeys)

    # For each of the combined possible key, try to validate the message
    # decrypted with it
    for index in itertools.product(range(NUM_HIGH_FREQ_MATCH_KEYS), repeat=key_len):
        key = []
        for i in range(len(index)):
            key.append(subkeys[i][index[i]][0])
        key = ''.join(key)
        if DEBUG > 0:
            print('Iterating possible key: %s' % key)
        decrypted = vigenere_cipher.decrypt(cipher_text, key)
        if DEBUG > 1:
            print('Decrypted message:')
            print(decrypted[:200])
        if detectEnglish.isEnglish(decrypted):
            print('Possible hack with key %s' % key)
            print(decrypted[:200])
            print()
            print('Press D for done, or ENTER to continue')
            response = input('>>>>')
            if response.upper().startswith('D'):
                return decrypted

    # We have iterated all the possible keys of the given length but failed to
    # identify any English-like things, return out with None to denote failure
    return None


def hack(cipher_text):
    key_len_likely = _kasiski_examine(cipher_text)

    # First try the key lengths from Kasiski Examination
    for keylen in key_len_likely:
        decrypted = _attack_with_key_len(keylen, cipher_text)
        if decrypted is not None:
            return decrypted

    # If we reach here, we don't have a valid hack with keylens provided from
    # Kasiski Examination. Prompt the users for whether to continue
    print('We have run out of the likely key lengths reported by Kasiski exam')
    print('Do you want to brute-force the key length? (Y/N)')
    response = input('>>>>')
    if response.upper().startswith('N'):
        return None

    # Brute-forcing all the possible keylens except those already tested with
    # Kasiski method
    for keylen in range(1, MAX_KEY_LEN + 1):
        if keylen not in key_len_likely:
            decrypted = _attack_with_key_len(keylen, cipher_text)
            if decrypted is not None:
                return decrypted

    # Have to accept that we lose...
    return None


# Below starts testing code
def main():
    message = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi,
lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz
hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg
jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk
qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum.
Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg
(GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav
wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o
iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq
pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms
umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz
cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi
1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg,
ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe
avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at
hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce
Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a
tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn
wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm
tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz
1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn
avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk
jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt
uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby
gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa
at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd
yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    # message = """Tzx isnz eccjxkg nfq lol mys bbqq I lxcz."""
    decrypted = hack(message)
    if decrypted is not None:
        print('Decrypted message:')
        print(decrypted)
    else:
        print("Failed to hack the encryption")


if __name__ == '__main__':
    main()
