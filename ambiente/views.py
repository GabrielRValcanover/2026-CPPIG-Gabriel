
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import AmbienteModelForm
from .models import Ambiente


class AmbientesListView(ListView):
    model = Ambiente
    template_name = 'ambientes.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(AmbientesListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,1)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem ambientes cadastrados!')




class AmbienteAddView(SuccessMessageMixin,CreateView):
    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "ambiente Cadastrado com sucesso!"


class AmbienteUpdateView(SuccessMessageMixin,UpdateView):
    model = Ambiente
    form_class = AmbienteModelForm
    template_name = 'ambiente_form.html'
    success_url = reverse_lazy('ambientes')
    success_message = "Ambiente Atualizado com sucesso!"

class AmbienteDeleteView(SuccessMessageMixin,DeleteView):
    model = Ambiente
    template_name = 'ambientes_apagar.html'
    success_url = reverse_lazy('ambientes')
    success_message= "Ambiente Deletado com sucesso!"


