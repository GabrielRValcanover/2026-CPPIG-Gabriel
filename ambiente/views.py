from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from chaves.models import Chave

from .forms import AmbienteModelForm
from .models import Ambiente


class AmbientesListView(PermissionRequiredMixin,ListView):
    permission_required = 'ambiente.view_ambiente'
    permission_denied_message = 'Visualizar ambiente'
    model = Ambiente
    template_name = 'ambientes.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(AmbientesListView, self).get_queryset()
        if buscar:
            qs = qs.filter(models.Q(nome__icontains=buscar) | models.Q(nomenclatura__icontains=buscar)| models.Q(bloco__nome__icontains=buscar))

        if qs.count()>0:
          paginator = Paginator(qs,50)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
            messages.info(self.request,'Não existem ambientes cadastrados!')
            return qs




class AmbienteAddView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'ambiente.add_ambiente'
    permission_denied_message = 'Cadastrar ambiente'
    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "ambiente Cadastrado com sucesso!"

    def form_valid(self, form):
        response = super().form_valid(form)
        chave_mestra = Chave.objects.filter(bloco= self.object.bloco, tipo='mestra').first()
        if chave_mestra:
            chave_mestra.ambientes.add(self.object)
        return response




class AmbienteUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = 'ambiente.change_ambiente'
    permission_denied_message = 'Editar ambiente'

    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "Ambiente Atualizado com sucesso!"

class AmbienteDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = 'ambiente.delete_ambiente'
    permission_denied_message = 'Excluir ambiente'
    model = Ambiente
    template_name = 'ambientes_apagar.html'
    success_url = reverse_lazy('ambientes')
    success_message= "Ambiente Deletado com sucesso!"


