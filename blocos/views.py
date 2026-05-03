
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import BlocoModelForm
from .models import Bloco

class BlocoListView(ListView):
    model = Bloco
    template_name = 'blocos.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(BlocoListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,10)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem blocos cadastrados!')




class BlocoAddView(SuccessMessageMixin,CreateView):
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = "Bloco Cadastrado com sucesso!"


class BlocoUpdateView(SuccessMessageMixin,UpdateView):
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = "Bloco Atualizado com sucesso!"

class BlocoDeleteView(SuccessMessageMixin,DeleteView):
    model = Bloco
    template_name = 'bloco_apagar.html'
    success_url = reverse_lazy('blocos')
    success_message= "Bloco Deletado com sucesso!"


