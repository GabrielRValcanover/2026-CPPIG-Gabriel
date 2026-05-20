
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

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
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,50)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem ambientes cadastrados!')




class AmbienteAddView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'ambiente.add_ambiente'
    permissiom_denied_message = 'Cadastrar ambiente'
    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "ambiente Cadastrado com sucesso!"


class AmbienteUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = 'ambiente.update_ambiente'
    permissiom_denied_message = 'Editar ambiente'

    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "Ambiente Atualizado com sucesso!"

class AmbienteDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = 'ambiente.delete_ambiente'
    permissiom_denied_message = 'Excluir ambiente'
    model = Ambiente
    template_name = 'ambientes_apagar.html'
    success_url = reverse_lazy('ambientes')
    success_message= "Ambiente Deletado com sucesso!"


