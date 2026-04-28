from contextlib import redirect_stderr

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from chaves.forms import ChaveModelForm
from chaves.models import Chave
from ambiente.models import Ambiente
from blocos.models import Bloco
from .forms import ChaveModelForm

class ChavesListView(ListView):
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ChavesListView, self).get_queryset()


        if buscar:
            # qs = qs.filter(nome__icontains=buscar)
            qs = qs.filter(descricao__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 5)
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



class ChaveAmbienteAddView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave adicionada com sucesso no ambiente!'

    def form_valid(self, form):
        response = super().form_valid(form)
        ambiente = Ambiente.objects.get(id=self.kwargs['ambiente_id'])
        self.object.ambientes.add(ambiente)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ambiente'] = Ambiente.objects.get(id=self.kwargs['ambiente_id'])
        return context

class ChaveBlocoAddView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave do bloco adicionada com sucesso no bloco!'

    def form_valid(self, form):
        response = super().form_valid(form)
        ambientes = Ambiente.objects.filter(
            bloco_id=self.kwargs['bloco_id'])
        for ambiente in ambientes:
            self.object.ambientes.add(ambiente)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bloco'] = Bloco.objects.get(id=self.kwargs['bloco_id'])
        return context

def verificacaoChaves(request, tipo, id):

    if tipo == 'ambiente':
        chave = Chave.objects.filter(ambientes__id=id).first()

        if chave:
            return render(request, 'verifica_form.html', {'chave': chave})

        return redirect('chave_ambiente', ambiente_id=id)

    elif tipo == 'bloco':
        chave = Chave.objects.filter(ambientes__bloco__id=id).first()

        if chave:
            return render(request, 'verifica_form.html', {'chave': chave})

        return redirect('chave_bloco', bloco_id=id)

    return redirect('chaves')
