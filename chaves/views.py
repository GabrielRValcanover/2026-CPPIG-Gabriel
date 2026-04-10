from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from chaves.forms import ChaveModelForm
from chaves.models import Chave


class ChavesListView(ListView):
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ChavesListView, self).get_queryset()


        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem chaves cadastradas!')



class ChaveAddView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave adicionada com sucesso!'

class ChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chaves Alterada com sucesso!'

class ChaveDeleteView(SuccessMessageMixin, DeleteView):
    model = Chave
    template_name = 'chaves_apagar.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave excluída com sucesso!'

