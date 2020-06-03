# coding:UTF-8

import re

expressao_cpf = re.compile('^[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}$')

# http://www.pythonbrasil.com.br/moin.cgi/VerificadorDeCpf
"""
Este módulo fornece uma classe wrapper para ser usada com números de
CPF, que além de oferecer um método simples de verificação, também
conta com métodos para comparação e conversão.
>>> a = CPF('56068332551')
>>> b = CPF('560.683.325-51')
>>> c = CPF((1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0))
>>> assert a.valido()
>>> assert b.valido()
>>> assert not c.valido()
>>> assert a == b
>>> assert not b == c
>>> assert not a == c
>>> assert eval(repr(a)) == a
>>> assert eval(repr(b)) == b
>>> assert eval(repr(c)) == c
>>> assert str(a) == \"560.683.325-51\"
>>> assert str(b) == str(a)
>>> assert str(c) == \"123.456.789-00\"
"""


class CPF(object):

    def __init__(self, cpf):
        """Classe representando um número de CPF
        >>> a = CPF('95524361503')
        >>> b = CPF('955.243.615-03')
        >>> c = CPF([9, 5, 5, 2, 4, 3, 6, 1, 5, 0, 3])
        """
        try:
            basestring  # noqa
        except Exception:
            basestring = (bytes, str)

        if isinstance(cpf, basestring):
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")
            if not cpf.isdigit():
                raise ValueError("Valor não segue a forma xxx.xxx.xxx-xx")

        if len(cpf) != 11 and len(cpf) != 9:
            raise ValueError("O número de CPF deve ter 11 digítos")

        cpf = map(int, cpf)
        self.cpf = list(cpf)

    def __getitem__(self, index):
        """Retorna o dígito em index como string
        >>> a = CPF('95524361503')
        >>> a[9] == '0'
        True
        >>> a[10] == '3'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 3
        False
        """
        return str(self.cpf[index])

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:
        eval(repr(cpf)) == cpf
        >>> a = CPF('95524361503')
        >>> print(repr(a))
        CPF('95524361503')
        >>> eval(repr(a)) == a
        True
        """
        return "CPF('%s')" % ''.join([str(x) for x in self.cpf])

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF
        >>> a = CPF('95524361503')
        >>> b = CPF('955.243.615-03')
        >>> c = CPF('123.456.789-00')
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True
        """
        if isinstance(other, CPF):
            return self.cpf == other.cpf
        return False

    def __str__(self):
        """Retorna uma string do CPF na forma com pontos e traço
        >>> a = CPF('95524361503')
        >>> str(a)
        '955.243.615-03'
        """
        d = ((3, "."), (7, "."), (11, "-"))
        s = list(map(str, self.cpf))
        for i, v in d:
            s.insert(i, v)
        r = ''.join(s)
        return r

    def sem_formato(self):
        """Retorna uma string do CPF sem pontos e traço
        >>> a = CPF('95524361503')
        >>> a.sem_formato()
        '95524361503'
        """
        return "".join([str(x) for x in self.cpf])

    def valido(self):
        """Valida o número de cpf
        >>> a = CPF('95524361503')
        >>> a.valido()
        True
        >>> b = CPF('12345678900')
        >>> b.valido()
        False
        """

        if len(set(self.cpf)) == 1:
            return False

        cpf = self.cpf[:9]
        # pegamos apenas os 9 primeiros dígitos do cpf e geramos os
        # dois dígitos que faltam
        while len(cpf) < 11:

            r = sum(
                map(
                    lambda u: (len(cpf) + 1 - u[0]) * u[1],
                    enumerate(cpf)
                )
            ) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cpf.append(f)

        # se o número com os digítos faltantes coincidir com o número
        # original, então ele é válido
        return bool(cpf == self.cpf)

    def calcular_dv(self):
        cpf = self.cpf[:9]
        # pegamos apenas os 9 primeiros dígitos do cpf e geramos os
        # dois dígitos que faltam
        while len(cpf) < 11:

            r = sum(
                map(
                    lambda u: (len(cpf) + 1 - u[0]) * u[1],
                    enumerate(cpf)
                )
            ) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cpf.append(f)

        return ''.join(map(str, cpf[-2:]))

    def __nonzero__(self):
        """Valida o número de cpf
        >>> a = CPF('95524361503')
        >>> bool(a)
        True
        >>> b = CPF('12345678900')
        >>> bool(b)
        False
        >>> b = CPF('11111111111')
        >>> bool(b)
        False
        >>> if a:
        ...     print('OK')
        ...
        OK
        >>> if b:
        ...     print('OK')
        ...
        >>>
        """

        return self.valido()


if __name__ == "__main__":

    import doctest
    import sys
    doctest.testmod(sys.modules[__name__])
