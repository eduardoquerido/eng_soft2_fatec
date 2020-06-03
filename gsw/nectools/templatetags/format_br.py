# coding: utf-8

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def formata_cpf(cpf):
    return mark_safe(cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:])


def formata_cnpj(cnpj):
    return mark_safe(cnpj[0:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:])


def formata_cep(cep):
    return mark_safe(cep[0:5] + '-' + cep[5:])


@register.filter
def format_br(field):
    field = field or ''
    if len(field) == 11:
        return formata_cpf(field)
    elif len(field) == 14:
        return formata_cnpj(field)
    elif len(field) == 8:
        return formata_cep(field)
    return field
