import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    # message = """Alan Mathison Turing was a British mathematician,
# logician, cryptanalyst, and computer scientist. He was highly influential in
# the development of computer science, providing a formalisation of the concepts
# of "algorithm" and "computation" with the Turing machine. Turing is widely
# considered to be the father of computer science and artificial intelligence.
# During World War II, Turing worked for the Government Code and Cypher School
# (GCCS) at Bletchley Park, Britain's codebreaking centre. For a time he was head
# of Hut 8, the section responsible for German naval cryptanalysis. He devised a
# number of techniques for breaking German ciphers, including the method of the
# bombe, an electromechanical machine that could find settings for the Enigma
# machine. After the war he worked at the National Physical Laboratory, where he
# created one of the first designs for a stored-program computer, the ACE. In
# 1948 Turing joined Max Newman's Computing Laboratory at Manchester University,
# where he assisted in the development of the Manchester computers and became
# interested in mathematical biology. He wrote a paper on the chemical basis of
# morphogenesis, and predicted oscillating chemical reactions such as the
# Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's
# homosexuality resulted in a criminal prosecution in 1952, when homosexual acts
# were still illegal in the United Kingdom. He accepted treatment with female
# hormones (chemical castration) as an alternative to prison. Turing died in
# 1954, just over two weeks before his 42nd birthday, from cyanide poisoning. An
# inquest determined that his death was suicide; his mother and some others
# believed his death was accidental. On 10 September 2009, following an Internet
# campaign, British Prime Minister Gordon Brown made an official public apology
# on behalf of the British government for "the appalling way he was treated." As
# of May 2012 a private member's bill was before the House of Lords which would
# grant Turing a statutory pardon if enacted."""
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
    key = 'ASIMOV'
    # key = random_key(6)
    print('key: %s' % (key))
    print()
    # operation = 'encrypt'
    operation = 'decrypt'
    # print(encrypt(message, key))
    print(decrypt(message, key))


def encrypt(message, key):
    return _translate_message(message, key, 'encrypt')


def decrypt(message, key):
    return _translate_message(message, key, 'decrypt')


def _translate_message(message, key, mode):
    translated_message = ''
    index_subkey = 0
    for c in message:
        subkey = LETTERS.find(key[index_subkey].upper())
        if c.upper() in LETTERS:
            translated_message += _caesar_cipher_translate(c, subkey, mode)
            index_subkey = (index_subkey + 1) % len(key)
        else:
            translated_message += c
    return translated_message


def _caesar_cipher_translate(message, key, mode):
    translated_message = ''
    if mode == 'encrypt':
        for c in message:
            if c.upper() in LETTERS:
                if c.isupper():
                    translated_message += LETTERS[(LETTERS.find(c) + key) % len(LETTERS)]
                else:
                    translated_message += LETTERS[(LETTERS.find(c.upper()) + key) % len(LETTERS)].lower()
            else:
                translated_message += c
    elif mode == 'decrypt':
        for c in message:
            if c.upper() in LETTERS:
                if c.isupper():
                    translated_message += LETTERS[(LETTERS.find(c) - key) % len(LETTERS)]
                else:
                    translated_message += LETTERS[(LETTERS.find(c.upper()) - key) % len(LETTERS)].lower()
            else:
                translated_message += c
    else:
        return None
    return translated_message


def random_key(key_len):
    key_list = [''] * key_len
    for i in range(key_len):
        key_list[i] = LETTERS[random.randint(1, len(LETTERS))]
    return ''.join(key_list)


if __name__ == '__main__':
    main()
