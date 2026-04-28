from django.urls import path

from .views import (EmprestimoListView, EmprestimoAddView, EmprestimoUpdateView, EmprestimoDeleteView)

urlpatterns = [
    path('emprestimos/', EmprestimoListView.as_view(), name='emprestimos'),
    path('emprestimo/adicionar/', EmprestimoAddView.as_view(), name='emprestimo_adicionar'),
    path('<int:pk>/emprestimo/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
    path('<int:pk>/emprestimo/apagar/', EmprestimoDeleteView.as_view(), name='emprestimo_apagar'),

]
