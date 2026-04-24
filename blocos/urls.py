from django.urls import path

from .views import  BlocoAddView, BlocoUpdateView, BlocoDeleteView, BlocoListView

urlpatterns = [
    path('blocos', BlocoListView.as_view(), name='blocos'),
    path('blocos/adicionar/', BlocoAddView.as_view(), name='bloco_adicionar'),
    path('<int:pk>/bloco/editar/', BlocoUpdateView.as_view(), name='bloco_editar'),
    path('<int:pk>/bloco/apagar/', BlocoDeleteView.as_view(), name='bloco_apagar'),


]
