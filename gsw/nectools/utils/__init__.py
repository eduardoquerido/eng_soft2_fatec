import logging

from functools import reduce
from random import choice, randint


from django.conf import settings
from django.db.utils import DatabaseError


VOGAIS = 'AEIOUYaeiouy' * 5 + '!&0134@'
CONSOANTES = 'BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz' * 3 + '256789_'


logger = logging.getLogger(__name__)


class Echo:
    def write(self, value):
        return value


def gera_password(min_len=14, max_len=19):
    c = (lambda x: x % 2 == 0 and choice(CONSOANTES) or choice(VOGAIS))
    if min_len == max_len:
        length = min_len
    else:
        length = randint(min_len, max_len)
    return ''.join(c(i) for i in range(length))


def cursor_execute(cursor, sql):
    try:
        cursor.execute(sql)
    except (DatabaseError, Exception) as e:
        if settings.DEBUG:
            logger.warning('Erro ao executar um cursor! [%s]' % sql)
            return False
        raise e
    return True


def dictfetchall(cursor):
    desc = [col[0] for col in cursor.description]
    return [
        dict(zip(desc, row))
        for row in cursor.fetchall()
    ]


def listfetchall(cursor):
    "Return all rows from a cursor as a list"
    return [row[0] for row in cursor.fetchall()]


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


def get_hex(n, fill=2):
    '''
        recebe um número (boolean, int, float, long, string)
        e converte em um hexadecimal com o tamanho passado no 2
        parâmetro (default 2)
    '''
    return str(hex(int(n))[2:]).zfill(fill)


def multiple_replace(_str, _in, _out):
    '''
        recebe uma string e faz um multiple replace
        o segundo parâmetro é sempre uma lista de strings
        que serão trocadas pelas do 3 parâmetro

        o 2 e o 3 parâmetro tem q ter o mesmo tamanho

        o 3 parâmetro pode ser uma string, neste caso
        todas as strings do 2 parâmetro serão trocadas
        pela string o 3 parâmetro
    '''
    if isinstance(_out, (list, tuple)):
        if len(_out) != len(_in):
            raise ValueError('len(_in) != len(_out)')
    elif isinstance(_out, str):
        _out = [_out for _ in _in]
    return reduce(lambda s, r: str.replace(s, r[1], _out[r[0]]), enumerate(_in), str(_str))


def join_strs(s, itens):
    return s.join(map(str, [i for i in itens if i]) if itens else [''])


def kml_to_rgba(kml):
    return 'rgba(%s,%s,%s,%s)' % (
        int(kml[6:], 16),
        int(kml[4:6], 16),
        int(kml[2:4], 16),
        str(int(kml[:2], 16) / 255.0)[0:4]
    )


def rgba_to_kml(rgba):
    '''
        pega um rgba e retorna uma cor em KML
        exemplo:
            rgba(25,5,255,1)
            FFFF0519
        cores em KML são
        AABBGGRR
    '''
    comp = map(
        float,
        multiple_replace(
            str(rgba),
            [u'rgba(', u')', u' '],
            u''
        ).split(u',')
    )
    return reduce(
        str.__add__,
        map(get_hex, comp[:3][::-1]),
        get_hex(min(1, max(0, comp[3])) * 255)
    ).upper()


def dedupe(items):
    '''
        retorna itens não duplicados mantendo a ordem dos items.
        Não foi utilizado set porque ele não mantem a ordem.
        Obs.: esse codigo funciona apenas para itens de sequencia passíveis de hashing.
        Se necessário implementar para qualquer item alterar cod da seguinte forma:
    '''
    #     val = item if key is None else key(item)
    #     if val not in seen:
    #         yield item
    #         seen.add(val)

    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


def memoize(f):
    memo = {}

    def inner(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return inner


def random_char_challenge():
    '''
    Função q gera uma string aleatória
    usado para gerar a palavra do captcha
    '''
    chars, ret = 'abcdefghijklmnopqrstuvwxyz0123456789', ''
    for i in range(settings.CAPTCHA_LENGTH):
        ret += choice(chars)
    return ret.upper(), ret


def clean_mask(_str):
    if _str:
        return _str.replace(' ', '').replace('.', '').replace('-', '').replace('/', '').replace('(', '').replace(')', '')
    return _str
