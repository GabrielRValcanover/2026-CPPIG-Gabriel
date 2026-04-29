from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import CopiaChave
from .forms import CopiaChaveModelForm

class CopiaChaveListView(ListView):
    model = CopiaChave
    template_name = 'copias.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('chave')

        if buscar:
            qs = qs.filter(
                Q(identificador__icontains=buscar)| Q(chave__descricao__icontains=buscar)
            )

        if qs.count() > 0:
            paginator = Paginator(qs, 3)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Copias de chaves cadastradas! ')



class CopiaChaveAddView(SuccessMessageMixin, CreateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_chave_form.html'
    success_url = reverse_lazy('copia_chaves')
    success_message = 'Cópia criada com sucesso!'



class CopiaChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_chave_form.html'
    success_url = reverse_lazy('copia_chaves')
    success_message = 'Cópia atualizada com sucesso!'



class CopiaChaveDeleteView(SuccessMessageMixin, DeleteView):
    model = CopiaChave
    template_name = 'copia_chave_apagar.html'
    success_url = reverse_lazy('copia_chaves')
    success_message = 'Cópia excluída com sucesso!'