# -*- coding: utf-8 -*-
from core import menu_mixin
from tools.views import base as tools_views
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from vagas.forms import (VagasForm, VagasSearchForm)
from vagas.models import Vagas


class VagasListView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseListView
):
    filter_by_user = False
    permission_required = ''
    form_class = VagasSearchForm
    current_section = 'vagas'
    sub_current_section = 'vaga'


class VagasCreateView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseCreateView
):
    filter_by_user = False
    permission_required = ''
    current_section = 'vagas'
    sub_current_section = 'vaga'
    model = Vagas
    form_class = VagasForm


class VagasUpdateView(
    menu_mixin.ProjetoMenuMixin,
    tools_views.BaseUpdateView
):
    filter_by_user = False
    detail_url = False
    permission_required = ''
    current_section = 'vagas'
    sub_current_section = 'vaga'
    model = Vagas
    form_class = VagasForm
