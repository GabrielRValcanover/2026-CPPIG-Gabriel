from django.urls import path

from .views import ChavesListView, ChaveAddView, ChaveUpdateView, ChaveDeleteView, ChaveAmbienteAddView, ChaveBlocoAddView,verificacaoChaves

urlpatterns = [
    path('chaves/', ChavesListView.as_view(), name='chaves'),
    path('chaves/adicionar/', ChaveAddView.as_view(), name='chaves_adicionar'),
    path('<int:pk>/chave/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/chave/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
    path('chave_ambiente/<int:ambiente_id>/', ChaveAmbienteAddView.as_view(), name='chave_ambiente'),
    path('chave_bloco/<int:bloco_id>/', ChaveBlocoAddView.as_view(), name='chave_bloco'),
    path('verificar/<str:tipo>/<int:id>/', verificacaoChaves, name='verificar_chave'),
]
