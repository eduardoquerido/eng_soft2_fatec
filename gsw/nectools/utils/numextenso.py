# coding: utf-8

# Autor: Fabiano Weimar dos Santos (xiru)
# Correcao em 20080407: Gustavo Henrique Cervi (100:"cento") => (1:"cento')

import sys

ext = [
    {
        0: '', 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco',
        6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
        11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze',
        16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove'
    },
    {
        2: 'vinte', 3: 'trinta', 4: 'quarenta', 5: 'cinquenta',
        6: 'sessenta', 7: 'setenta', 8: 'oitenta', 9: 'noventa'
    },
    {
        1: 'cento', 2: 'duzentos', 3: 'trezentos',
        4: 'quatrocentos', 5: 'quinhentos', 6: 'seiscentos',
        7: 'setecentos', 8: 'oitocentos', 9: 'novecentos'
    }
]

und = [
    '', ' mil',
    (' milhão', ' milhões'),
    (' bilhão', ' bilhões'),
    (' trilhão', ' trilhões')
]

UNIDADE_NAMES = {
    'reais': {
        'plural': ('reais', 'centavos'),
        'singular': ('real', 'centavo')
    },
    'ha': {
        'plural': ('hectares', 'ares', 'centiares'),
        'singular': ('hectare', 'are', 'centiare')
    },
}


def cent(s, grand):
    s = '0' * (3 - len(s)) + s
    if s == '000':
        return ''
    if s == '100':
        return 'cem'
    ret = ''
    dez = s[1] + s[2]
    if s[0] != '0':
        ret += ext[2][int(s[0])]
        if dez != '00':
            ret += ' e '
    if int(dez) < 20:
        ret += ext[0][int(dez)]
    else:
        if s[1] != '0':
            ret += ext[1][int(s[1])]
            if s[2] != '0':
                ret += ' e ' + ext[0][int(s[2])]

    return ret + (type(und[grand]) == tuple and (int(s) > 1 and und[grand][1] or und[grand][0]) or und[grand])


def extenso(n):
    sn = str(int(n))
    ret = []
    grand = 0
    while sn:
        s = sn[-3:]
        sn = sn[:-3]
        ret.append(cent(s, grand))
        grand += 1
    ret.reverse()
    return ' e '.join([r for r in ret if r])


def ha_extenso(n):
    '''hectare por extenso'''

    sn = '%.4f' % float(n)
    num, dec = sn.split('.')
    num_plural = int(num) != 1
    num_sufixo = UNIDADE_NAMES['ha'][num_plural and 'plural' or 'singular'][0]
    _return = []

    if num != '0':
        _return.append('%s %s' % (extenso(num), num_sufixo))

    if dec != '0000':
        part1, part2 = str(dec)[:2], str(dec)[2:]
        if part1 != '00':
            dec_plural = int(part1) != 1
            part1_sufixo = UNIDADE_NAMES['ha'][dec_plural and 'plural' or 'singular'][1]
            _return.append('%s %s' % (extenso(part1), part1_sufixo))
        if part2 != '00':
            dec_plural = int(part2) != 1
            part2_sufixo = UNIDADE_NAMES['ha'][dec_plural and 'plural' or 'singular'][2]
            _return.append('%s %s' % (extenso(part2), part2_sufixo))

    return ' e '.join(_return)


def numero_extenso(n, unidade='reais'):
    if not unidade:
        return extenso(n)
    if unidade == 'ha':
        return ha_extenso(n)
    sn = '%.2f' % float(n)
    num, dec = sn.split('.')
    num_plural = int(num) != 1
    num_sufixo = UNIDADE_NAMES[unidade][num_plural and 'plural' or 'singular'][0]
    ret = '%s %s' % (extenso(num), num_sufixo)
    if dec != '00':
        dec_plural = int(dec) != 1
        dec_sufixo = UNIDADE_NAMES[unidade][dec_plural and 'plural' or 'singular'][1]
        ret += ' e %s %s' % (extenso(dec), dec_sufixo)
    return ret


if __name__ == '__main__':

    if len(sys.argv) >= 3:
        n = sys.argv[1]
        e = numero_extenso(n, sys.argv[2])
        print(n)
        print(e)

    elif len(sys.argv) == 2:
        n = sys.argv[1]
        e = numero_extenso(n)
        print(n)
        print(e)

    else:
        # testes
        for num in range(100, 150):
            for d in range(0, 100):
                n = '%s.%s' % (num, d)
                print(n, '\t', numero_extenso(n))
