from core import models
from nectools import forms as nectools_forms


class UserSearchForm(nectools_forms.BaseSearchForm):
    class Meta:
        base_qs = models.User.objects.filter(
            is_active=True
        )
        search_fields = [
            'nome',
            'email',
        ]
