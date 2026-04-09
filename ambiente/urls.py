from django.urls import path

from .views import AmbientesListView, AmbienteAddView, AmbienteUpdateView,AmbienteDeleteView

urlpatterns = [
    path('ambientes', AmbientesListView.as_view(), name='ambientes'),
    path('ambientes/adicionar/', AmbienteAddView.as_view(), name='ambiente_adicionar'),
    path('<int:pk>/ambiente/editar/', AmbienteUpdateView.as_view(), name='ambiente_editar'),
    path('<int:pk>/ambiente/apagar/', AmbienteDeleteView.as_view(), name='ambiente_apagar'),
]
