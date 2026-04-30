from django.urls import path
from .views import ReservaListView, ReservaAddView, ReservaUpdateView, ReservaDeleteView

urlpatterns = [
    path('reservas/', ReservaListView.as_view(), name='reservas'),
    path('reservas/adicioanr/', ReservaAddView.as_view(), name='reserva-adicionar'),
    path('reservas/<int:pk>/editar/', ReservaUpdateView.as_view(), name='reserva-editar'),
    path('reservas/<int:pk>/apagar/', ReservaDeleteView.as_view(), name='reserva-apagar'),
]