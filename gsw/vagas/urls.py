from django.urls import include, path
from vagas import views

urlpatterns = [
    path('vagas/', include([
        path(
            '',
            views.VagasListView.as_view(),
            name='vagas_list'
        ),
        path(
            'novo/',
            views.VagasCreateView.as_view(),
            name='vagas_form'
        ),
        # path(
        #     'json/',
        #     views.autofill_campos_ocupacaoimovel,
        #     name='resposta_json'
        # ),
        path(
            '<int:pk>/',
            views.VagasUpdateView.as_view(),
            name='vagas_form'
        ),
    ])),
]
