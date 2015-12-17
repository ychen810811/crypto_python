# -*- coding:utf-8 -*-

import re
import pprint
import math

import vigenere_cipher
import freq_analysis
import detectEnglish

LETTERS = vigenere_cipher.LETTERS
REGEX_NON_LETTERS = re.compile('[^A-Z]')

MAX_KEY_LEN = 16
MIN_SEQ_FREQ = 4  # will not consider seq's repeating for less than this many of times


# Find repeated letter sequences thru the message and return a dict value with
# keys of the seq's and values of lists of the spacings.
def _repeated_seq_spacing(message):
    message = REGEX_NON_LETTERS.sub('', message.upper())
    seq_spacing = {}
    for len_seq in range(3, 6):
        for i in range(len(message) - len_seq):
            seq = message[i:i+len_seq]
            for j in range(i+len_seq, len(message)-len_seq):
                if seq == message[j:j+len_seq]:
                    if seq not in seq_spacing:
                        seq_spacing[seq] = [j-i]
                    else:
                        seq_spacing[seq].append(j-i)
    return seq_spacing


def _factors(number):
    f = []
    for n in range(2, math.sqrt(number)):
        if number % n == 0:
            f.append(n)
    return f



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
    # message = """Ppqca xqvekg ybnkmazu ybngbal jon i tszm jyim. Vrag voht vrau c tksg. Ddwuo xitlazu vavv
# raz c vkb qp iwpou."""
    pprint.pprint(_repeated_seq_spacing(message))


if __name__ == '__main__':
    main()
