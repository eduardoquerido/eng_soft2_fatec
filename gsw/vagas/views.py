# -*- coding: utf-8 -*-
from core import menu_mixin
from tools.views import base as tools_views
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from vagas.forms import (VagaForm, VagaSearchForm)
from vagas.models import Vaga


class VagaListView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseListView
):
    filter_by_user = False
    permission_required = ''
    form_class = VagaSearchForm
    current_section = 'vagas'
    sub_current_section = 'vaga'


class VagaCreateView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseCreateView
):
    filter_by_user = False
    permission_required = ''
    current_section = 'vagas'
    sub_current_section = 'vaga'
    model = Vaga
    form_class = VagaForm


class VagaUpdateView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseUpdateView
):
    filter_by_user = False
    detail_url = False
    permission_required = ''
    current_section = 'vagas'
    sub_current_section = 'vaga'
    model = Vaga
    form_class = VagaForm

