from django import forms
from tools import forms as tools_forms
from vagas.models import (Vaga, Competencia, Candidato, Habilidade)
from django_select2.forms import ModelSelect2MultipleWidget
from vagas.choices import (BENEFICIOS)


class VagaSearchForm(tools_forms.BaseSearchForm):
    class Meta:
        base_qs = Vaga.objects.filter()
        search_fields = [
            'nome_vaga',
            'id_vaga',
        ]


class VagaForm(
    forms.ModelForm
):

    beneficios = forms.MultipleChoiceField(
        choices=BENEFICIOS,
        widget=forms.CheckboxSelectMultiple,
    )

    competencia = forms.ModelMultipleChoiceField(
        queryset=Competencia.objects.all(),
        required=True,
        widget=ModelSelect2MultipleWidget(
            model=Competencia,
            search_fields=[
                'nome__icontains',
            ]
        )
    )

    class Meta:
        model = Vaga
        fields = [
            'id_vaga',
            'nome_vaga',
            'qtd_vaga',
            'categoria',
            'cidade',
            'competencia',
            'horario_trab',
            'descricao',
            'exp_requerida',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        super(VagaForm, self).__init__(*args, **kwargs)
        self.fields['id_vaga'].widget.attrs['placeholder'] = '2020/001'


class CompetenciaSearchForm(tools_forms.BaseSearchForm):
    class Meta:
        base_qs = Competencia.objects.filter()
        search_fields = [
            'nome__icontains',
            'nivel_icontains',
        ]


class CompetenciaForm(
    forms.ModelForm
):

    class Meta:
        model = Competencia
        fields = [
            'nome',
            'nivel'
        ]


class CandidatoSearchForm(tools_forms.BaseSearchForm):
    class Meta:
        base_qs = Candidato.objects.filter()
        search_fields = [
            'nome__icontains',
            'cpf__icontains',
        ]


class CandidatoForm(
    forms.ModelForm
):

    class Meta:
        model = Candidato
        fields = [
            'nome',
            'sexo',
            'email',
            'cpf',
            'ddd',
            'celular',
            'ddd2',
            'telefone',
            'rua',
            'bairro',
            'cidade',
            'numero_end',
            'complemento',
            'estado',
            'curriculo',
            'habilidades',
            'observacoes'
        ]


class HabilidadeSearchForm(tools_forms.BaseSearchForm):
    class Meta:
        base_qs = Habilidade.objects.filter()
        search_fields = [
            'nome__icontains',
        ]


class HabilidadeForm(
    forms.ModelForm
):

    class Meta:
        model = Habilidade
        fields = [
            'nome',
            'tipo'
        ]
