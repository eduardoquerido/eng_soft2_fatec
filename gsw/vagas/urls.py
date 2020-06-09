from django.urls import include, path
from vagas import views

urlpatterns = [
    path('vagas/', include([
        path(
            '',
            views.VagaListView.as_view(),
            name='vaga_list'
        ),
        path(
            'novo/',
            views.VagaCreateView.as_view(),
            name='vaga_form'
        ),
        # path(
        #     'json/',
        #     views.autofill_campos_ocupacaoimovel,
        #     name='resposta_json'
        # ),
        path(
            '<int:pk>/',
            views.VagaUpdateView.as_view(),
            name='vaga_form'
        ),
    ])),
]
