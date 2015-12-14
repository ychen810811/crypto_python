import os
import sys
import copy
import re
import pprint
import simpleSubCipher
import makeWordPatterns

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main()

import wordPatterns    # now we have allPatterns dictionary value

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PATTERN_NOT_LETTER_OR_SPACE = re.compile('[^A-Z\s]')


def main():
    message = """Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr
sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr
pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr
pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr
sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py
nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm"""
    # message = "OLQIHXIRCKGNZ PLQRZKBZB MPBKSSIPLC"
#     message = """S ln lmcaloh ylc xpcji py Mpxopx, lxo lr S elmk sx jia rjcaajr py
# Bajacrftcui, S yaam l wpmo xpcjiacx fcaaza bmlh tbpx nh wiaakr, eiswi
# fclwar nh xacqar lxo ysmmr na esji oamsuij.  Op hpt txoacrjlxo jisr
# yaamsxu?  Jisr fcaaza, eiswi ilr jclqammao ycpn jia causpxr jpelcor
# eiswi S ln loqlxwsxu, usqar na l ypcajlrja py jipra swh wmsnar.
# Sxrbscsjao fh jisr esxo py bcpnsra, nh olhocalnr fawpna npca yacqaxj
# lxo qsqso.  S jch sx qlsx jp fa bacrtloao jilj jia bpma sr jia ralj py
# ycprj lxo oarpmljspx; sj aqac bcaraxjr sjramy jp nh snlusxljspx lr jia
# causpx py faltjh lxo oamsuij.  Jiaca, Nlculcaj, jia rtx sr ypcaqac
# qsrsfma, sjr fcplo osrk vtrj rkscjsxu jia ipcszpx lxo osyytrsxu l
# bacbajtlm rbmaxoptc.  Jiaca--ypc esji hptc malqa, nh rsrjac, S esmm btj
# rpna jctrj sx bcawaosxu xlqsuljpcr--jiaca rxpe lxo ycprj lca flxsriao;
# lxo, rlsmsxu pqac l wlmn ral, ea nlh fa elyjao jp l mlxo rtcblrrsxu sx
# epxoacr lxo sx faltjh aqach causpx isjiacjp osrwpqacao px jia ilfsjlfma
# umpfa.  Sjr bcpotwjspxr lxo yaljtcar nlh fa esjiptj aglnbma, lr jia
# biaxpnaxl py jia ialqaxmh fposar txoptfjaomh lca sx jipra txosrwpqacao
# rpmsjtoar.  Eilj nlh xpj fa agbawjao sx l wptxjch py ajacxlm msuij?  S
# nlh jiaca osrwpqac jia epxocptr bpeac eiswi ljjclwjr jia xaaoma lxo nlh
# cautmlja l jiptrlxo wamarjslm pfracqljspxr jilj cadtsca pxmh jisr
# qphlua jp caxoac jiasc raansxu awwaxjcswsjsar wpxrsrjaxj ypcaqac.  S
# rilmm rljslja nh lcoaxj wtcsprsjh esji jia rsuij py l blcj py jia epcmo
# xaqac faypca qsrsjao, lxo nlh jcalo l mlxo xaqac faypca snbcsxjao fh
# jia yppj py nlx. Jiara lca nh axjswanaxjr, lxo jiah lca rtyyswsaxj jp
# wpxdtac lmm yalc py olxuac pc oalji lxo jp sxotwa na jp wpnnaxwa jisr
# mlfpcsptr qphlua esji jia vph l wismo yaamr eiax ia anflckr sx l msjjma
# fplj, esji isr ipmsolh nljar, px lx agbaosjspx py osrwpqach tb isr
# xljsqa csqac. Ftj rtbbprsxu lmm jiara wpxvawjtcar jp fa ylmra, hpt
# wlxxpj wpxjarj jia sxarjsnlfma faxaysj eiswi S rilmm wpxyac px lmm
# nlxksxo, jp jia mlrj uaxacljspx, fh osrwpqacsxu l blrrlua xalc jia bpma
# jp jipra wptxjcsar, jp calwi eiswi lj bcaraxj rp nlxh npxjir lca
# cadtsrsja; pc fh lrwacjlsxsxu jia rawcaj py jia nluxaj, eiswi, sy lj
# lmm bprrsfma, wlx pxmh fa ayyawjao fh lx txoacjlksxu rtwi lr nsxa."""
    mapping = hack(message)
    if os.path.exists('sub_cipher_key_mapping.txt'):
        print('\'sub_cipher_key_mapping.txt\' already exists, overwite? (y/n)')
        response = input('>>')
        if not response.lower().startswith('y'):
            sys.exit('Abort execution')
    fo = open('sub_cipher_key_mapping.txt', 'w')
    fo.write(pprint.pformat(mapping))
    fo.close

    print()
    print('Message:')
    print(message)
    print()
    key = gen_key(mapping)
    print('Key: %s' % (key))
    translated = simpleSubCipher.decryptMessage(key, message)
    print('Translated:')
    print(translated)


def hack(cipher_text):
    list_cipher_words = PATTERN_NOT_LETTER_OR_SPACE.sub('', cipher_text.upper()).split()
    mapping = _blank_letter_mapping()

    for cipher_word in list_cipher_words:
        mapping_new = _blank_letter_mapping()
        pattern_new = makeWordPatterns.makeWordPattern(cipher_word)
        if pattern_new not in wordPatterns.allPatterns:
            continue    # we have nothing to do with this cipher word
        else:
            for candidate in wordPatterns.allPatterns[pattern_new]:
                _add_mapping(mapping_new, cipher_word, candidate)
        _intersect_mapping(mapping, mapping_new)

    _remove_resolved_letter(mapping)
    return mapping


def _blank_letter_mapping():
    r = {}
    for c in LETTERS:
        r[c] = []
    return r


def _add_mapping(mapping, cipher_word, candidate):
    for i in range(len(cipher_word)):
        if i >= len(candidate):    # this should never happen - just ignore the remaining of the candidate string
            return
        if cipher_word[i] not in mapping:
            mapping[cipher_word[i]] = [candidate[i]]
        else:
            if candidate[i] not in mapping[cipher_word[i]]:
                mapping[cipher_word[i]].append(candidate[i])


def _intersect_mapping(mapping_dest, mapping_src):
    for c in mapping_src:
        if mapping_dest[c] == []:
            mapping_dest[c] += mapping_src[c]
        elif mapping_src[c] == []:
            continue
        else:
            for d in copy.deepcopy(mapping_dest[c]):
                if d not in mapping_src[c]:
                    while d in mapping_dest[c]:
                        mapping_dest[c].remove(d)


def _remove_resolved_letter(mapping):
    loop_flag = True
    while loop_flag:
        loop_flag = False
        for c in mapping:
            if len(mapping[c]) == 1:
                letter = mapping[c][0]
                for d in mapping:
                    if len(mapping[d]) > 1 and d != c and letter in mapping[d]:
                        mapping[d].remove(letter)
                        loop_flag = True


def decrypt(message, mapping):
    decrypted = ''
    for c in message:
        if c.upper() not in mapping:
            decrypted += c
        else:
            if len(mapping[c.upper()]) > 1:
                decrypted += '_'
            elif len(mapping[c.upper()]) == 0:
                decrypted += c
            else:
                if c.isupper():
                    decrypted += mapping[c][0]
                else:
                    decrypted += mapping[c.upper()][0].lower()
    return decrypted


def gen_key(mapping):
    list_key = [''] * len(simpleSubCipher.LETTERS)
    for c in mapping:
        if len(mapping[c]) == 1:
            list_key[simpleSubCipher.LETTERS.find(mapping[c][0])] = c
    for i in range(len(list_key)):
        if list_key[i] == '':
            list_key[i] = '_'
    # print('Final key is %s' % (pprint.pformat(list_key)))
    return ''.join(list_key)


if __name__ == '__main__':
    main()
