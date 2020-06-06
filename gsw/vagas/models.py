from django.db import models

from vagas.choices import (CATEGORIAS, BENEFICIOS, HORARIO_TRAB, ESTADOS)
from core.models import (UserAdd, UserUpd)


class Competencia(UserAdd, UserUpd):
    nome = models.CharField(
        max_length=20,
        blank=False,
        null=False
    )

class Vagas(UserAdd, UserUpd):

    STATUS = [
        (1, "Ativo"),
        (2, "Inativo"),
    ]

    id_vaga = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        unique=True
    )
    status = models.SmallIntegerField(choices=STATUS)
    nome_vaga = models.CharField(max_length=100, blank=False, null=False)
    qtd_vaga = models.SmallIntegerField(blank=False, null=False)
    competencia = models.ForeignKey(
        'Competencia',
        blank=False,
        null=False,
        on_delete=models.PROTECT
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        blank=False,
        null=False,
    )
    cidade = models.SmallIntegerField(
        choices=ESTADOS,
        blank=False,
        null=False)
    horario_trab = models.SmallIntegerField(
        choices=HORARIO_TRAB,
        blank=True,
        null=True
    )
    beneficios = models.SmallIntegerField(
        choices=BENEFICIOS,
        blank=True,
        null=True,
        default=None,
    )
    descricao = models.TextField(blank=False, null=False)
    exp_requerida = models.TextField(blank=False, null=False)
