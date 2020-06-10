from django import forms
from tools import forms as tools_forms
from vagas.models import (Vaga, Competencia)
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
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
            'horario_trab',
            'descricao',
            'exp_requerida',
            'status'
        ]

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