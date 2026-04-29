from django.urls import path

from .views import (CopiaChaveListView, CopiaChaveUpdateView, CopiaChaveDeleteView, CopiaChaveAddView, )


urlpatterns = [
    path('copia_chaves/', CopiaChaveListView.as_view(), name='copia_chaves'),
    path('copia_chaves/adicionar/', CopiaChaveAddView.as_view(), name='copia_chaves_adicionar'),
    path('<int:pk>/copia_chaves/editar/', CopiaChaveUpdateView.as_view(), name='copia_chaves_editar'),
    path('<int:pk>/copia_chaves/apagar/', CopiaChaveDeleteView.as_view(), name='copia_chaves_apagar'),
]