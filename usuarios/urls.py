from django.urls import path

from .views import UsuariosListView, UsuarioAddView, UsuarioUpdateView, UsuarioDeleteView

urlpatterns = [
    path('usuarios', UsuariosListView.as_view(), name='usuarios'),
    path('usuario/adicionar/', UsuarioAddView.as_view(), name='usuario_adicionar'),
    path('<int:pk>/usuario/editar/', UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('<int:pk>/usuario/apagar/', UsuarioDeleteView.as_view(), name='usuario_apagar'),
]