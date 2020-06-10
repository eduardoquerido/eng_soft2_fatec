from django.db import models

from vagas.choices import (CATEGORIAS, BENEFICIOS, HORARIO_TRAB, ESTADOS)
from core.models import (UserAdd, UserUpd)


class Competencia(UserAdd, UserUpd):
    
    class Nivel:
        AVANCADO = 1
        INTERMEDIARIO = 2
        BASICO = 3
        choices = [
            (1, 'Avançado'),
            (2, 'Intermediário'),
            (3, 'Básico'),
        ]
    
    nome = models.CharField(
        max_length=20,
        blank=False,
        null=False
    )
    nivel = models.SmallIntegerField(
        choices=Nivel.choices
    )

    def __str__(self):
        return self.nome

class Vaga(UserAdd, UserUpd):

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
    nome_vaga = models.CharField(
        verbose_name="Denominação da Vaga",
        max_length=100,
        blank=False,
        null=False
    )
    qtd_vaga = models.SmallIntegerField(
        verbose_name="Quantidade de vagas",
        blank=False,
        null=False
    )
    competencia = models.ManyToManyField('Competencia')
    categoria = models.SmallIntegerField(
        choices=CATEGORIAS,
        blank=False,
        null=False,
    )
    cidade = models.SmallIntegerField(
        verbose_name="Estado em que a vaga se encontra",
        choices=ESTADOS,
        blank=False,
        null=False)
    horario_trab = models.SmallIntegerField(
        verbose_name="Período",
        choices=HORARIO_TRAB,
        blank=True,
        null=True
    )
    beneficios = models.SmallIntegerField(
        choices=BENEFICIOS,
        blank=True,
        null=True,
    )
    descricao = models.TextField(
        verbose_name="Descrição da Vaga",
        blank=False,
        null=False
    )
    exp_requerida = models.TextField(
        verbose_name="Experiências necessárias",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome_vaga