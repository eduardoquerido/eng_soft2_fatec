# coding: utf-8
from django.db.models import Case, CharField, Value, When


def generate_cases_for_choices(query_field, choices, default=Value(u'[valor não encontrado]'), output_field=CharField()):
    '''
    Returns a Case expression based on a model's field and a list of choices tuple
    Autors:
        @mcrosariol
        @zokis
    '''
    return Case(
        default=default,
        output_field=output_field,
        *[
            When(**{query_field: value, 'then': Value(string)})
            for value, string in choices
        ]
    )
