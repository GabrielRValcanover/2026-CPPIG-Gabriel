
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import BlocoModelForm
from .models import Bloco

class BlocoListView(PermissionRequiredMixin,ListView):
    permission_required = 'blocos.view_bloco'
    permission_denied_message = 'Visualizar bloco'
    model = Bloco
    template_name = 'blocos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().prefetch_related('ambientes__chaves')
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() == 0:
           messages.info(self.request, 'Não existem blocos cadastrados!')

        paginator = Paginator(qs, 10)
        listagem = paginator.get_page(self.request.GET.get('page'))
        return listagem


class BlocoAddView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'blocos.add_bloco'
    permission_denied_message = 'Cadastrar bloco'
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = "Bloco Cadastrado com sucesso!"


class BlocoUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = 'blocos.change_bloco'
    permission_denied_message = 'Editar bloco'
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = "Bloco Atualizado com sucesso!"

class BlocoDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = 'blocos.delete_bloco'
    permission_denied_message= 'Excluir bloco'
    model = Bloco
    template_name = 'bloco_apagar.html'
    success_url = reverse_lazy('blocos')
    success_message= "Bloco Deletado com sucesso!"


