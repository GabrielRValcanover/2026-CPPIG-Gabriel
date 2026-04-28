
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import EmprestimoModelForm
from .models import Emprestimo

class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(EmprestimoListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,2)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem emprestomos cadastrados!')




class EmprestimoAddView(SuccessMessageMixin,CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Cadastrado com sucesso!"


class EmprestimoUpdateView(SuccessMessageMixin,UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Atualizado com sucesso!"

class EmprestimoDeleteView(SuccessMessageMixin,DeleteView):
    model = Emprestimo
    template_name = 'emprestimos_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message= "Emprestimo Deletado com sucesso!"


