# -*- coding: utf-8 -*-

from core import forms, menu_mixin, models
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from nectools.views import JSONResponseView
from nectools.views import base as nectools_views
from nectools.views import mixins as nectools_mixins


def logout_view(request):
    logout(request)
    return redirect('/')


class Home(menu_mixin.ProjetoMenuMixin, nectools_views.BaseNectoView, TemplateView):
    template_name = 'home.html'
    current_section = 'home'


class UserListView(menu_mixin.ProjetoMenuMixin, nectools_views.NectoListView):
    filter_by_user = False
    permission_required = ''
    form_class = forms.UserSearchForm
    current_section = 'administracao'
    sub_current_section = 'usuarios'


class UserCreateView(menu_mixin.ProjetoMenuMixin, nectools_views.NectoCreateView):
    filter_by_user = False
    permission_required = ''
    current_section = 'administracao'
    sub_current_section = 'usuarios'
    model = models.User
    fields = [
        'email',
        'nome',
        'is_active',
        'is_staff',
        'password',
    ]


class UserUpdateView(menu_mixin.ProjetoMenuMixin, nectools_views.NectoUpdateView):
    filter_by_user = False
    detail_url = False
    permission_required = ''
    current_section = 'administracao'
    sub_current_section = 'usuarios'
    model = models.User
    fields = [
        'email',
        'nome',
        'is_active',
        'is_staff',
        'password',
    ]
