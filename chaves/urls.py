from django.urls import path

from .views import ChavesListView, ChaveAddView, ChaveUpdateView, ChaveDeleteView

urlpatterns = [
    path('chaves', ChavesListView.as_view(), name='chaves'),
    path('chaves/adicionar/', ChaveAddView.as_view(), name='chave_adicionar'),
    path('<int:pk>/chave/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/chave/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
]

