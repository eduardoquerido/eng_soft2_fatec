from django import forms
from tools import forms as tools_forms
from vagas.models import (Vagas, Competencia)
from django_select2 import forms as ds2_forms
#from django_select2.forms import ModelSelect2MultipleWidget
from vagas.choices import (BENEFICIOS)


class VagasSearchForm(tools_forms.BaseSearchForm):
    class Meta:
        base_qs = Vagas.objects.filter()
        search_fields = [
            'nome_vaga',
            'id_vaga',
        ]


class VagasForm(
    forms.ModelForm
):

    beneficios = forms.MultipleChoiceField(
        choices=BENEFICIOS,
        widget=forms.CheckboxSelectMultiple,
    )

    competencia = forms.ModelMultipleChoiceField(
        queryset=Competencia.objects.all(),
        required=True,
        widget=ds2_forms.Select2MultipleWidget,
    )

    class Meta:
        model = Vagas
        fields = [
            'nome_vaga',
            'qtd_vaga',
            'categoria',
            'cidade',
            'horario_trab',
            'descricao',
            'exp_requerida',
            'status'
        ]
