from django.urls import reverse_lazy
from nectools.views.mixins import MenuMixin
from rules.contrib.views import PermissionRequiredMixin


class IterpiMenuMixin(MenuMixin, PermissionRequiredMixin):
    permission_required = 'true'

    def get_menu(self):
        return {
            'administracao': {
                'label': 'Administração',
                'perm': '',
                'icon': 'fa-cogs',
                'url': '#',
                'active': False,
                'subsections': [
                    ('usuarios', reverse_lazy('user_list'), 'Usuários', ''),
                ]
            },
            'Vaga': {
                'label': 'Vaga',
                'perm': '',
                'icon': 'fa-cogs',
                'url': '#',
                'active': False,
                'subsections': [
                #exemplo:
                    #('ocupacoes', reverse_lazy('ocupacaoimovel_list'), 'Ocupações', ''),
                ]
            }
        }
