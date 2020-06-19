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

        if self.nivel == 1:
            return self.nome + " (Avançado)"
        elif self.nivel == 2:
            return self.nome + " (Intermediário)"
        elif self.nivel == 3:
            return self.nome + " (Básico)"


class Habilidade(UserAdd, UserUpd):
    '''
    Essa classe serve para definir qual é e qual o tipo da skill que está sendo
    cadastrada, para posteriormente atribuí-las aos candidatos
    '''
    class Tipo:
        HARDSKILL = 1
        SOFTSKILL = 2
        choices = [
            (1, "Hard Skills"),
            (2, "Soft Skills")
        ]

    nome = models.CharField(
        verbose_name="Habilidade",
        max_length=20,
        blank=False,
        null=False
    )
    tipo = models.SmallIntegerField(
        choices=Tipo.choices,
        verbose_name="Tipo da Habilidade",
        blank=False,
        null=False
    )

    def __str__(self):
        return self.nome


class Candidato(UserUpd, UserAdd):

    class Sexo:
        MASCULINO = 1
        FEMININO = 2
        OUTROS = 3
        choices = [
            (1, 'Masculino'),
            (2, 'Feminino'),
            (3, 'Outros'),
        ]

    # Dados Cadastrais
    nome = models.CharField(
        verbose_name="Nome Completo",
        max_length=300,
        blank=False,
        null=False
    )
    sexo = models.SmallIntegerField(
        verbose_name="Gênero",
        choices=Sexo.choices
    )
    email = models.EmailField(
        verbose_name="E-mail"
    )
    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
        blank=False,
        null=False
    )
    ddd = models.CharField(
        verbose_name="DDD",
        max_length=4,
        blank=False,
        null=False
    )
    celular = models.CharField(
        verbose_name="Celular",
        max_length=10,
        blank=False,
        null=False
    )
    ddd2 = models.CharField(
        verbose_name="DDD",
        max_length=4,
        blank=True,
        null=True
    )
    telefone = models.CharField(
        verbose_name="Celular",
        max_length=10,
        blank=True,
        null=True
    )

    # Dados de endereço
    rua = models.CharField(
        verbose_name="Endereço",
        max_length=250,
        blank=False,
        null=False
    )
    bairro = models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    cidade = models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    numero_end = models.CharField(
        verbose_name="Número",
        max_length=250,
        blank=False,
        null=False
    )
    complemento = models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    estado = models.SmallIntegerField(
        verbose_name="Estado",
        choices=ESTADOS,
        blank=False,
        null=False
    )
    curriculo = models.FileField(
        verbose_name="",
        upload_to="documents/"
    )
    '''
    Os campos abaixo ficarão disponíveis somente ao pessoal de recrutamento,
    para adcionar ou remover habilidades que foram observadas nos candidatos durante o processo
    e para adicionar observações
    '''
    habilidades = models.ManyToManyField(
        'Habilidade',
        blank=True
    )
    observacoes = models.TextField(
        verbose_name="Observações sobre o candidato",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class Vaga(UserAdd, UserUpd):

    STATUS = [
        (1, "Ativo"),
        (2, "Inativo"),
    ]

    candidato = models.ManyToManyField(
        Candidato,
        verbose_name="Candidatos Cadastrados",
        blank=True,
    )
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
    competencia = models.ManyToManyField(
        Competencia,
        verbose_name="Competências da Vaga",
        blank=True,
    )
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
