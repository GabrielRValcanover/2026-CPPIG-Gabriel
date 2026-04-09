
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import UsuarioModelForm
from .models import Usuario


class UsuariosListView(ListView):
    model = Usuario
    template_name = 'usuarios.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(UsuariosListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,1)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem usuarios cadastrados!')




class UsuarioAddView(SuccessMessageMixin,CreateView):
    model = Usuario
    form_class = UsuarioModelForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuarios')
    success_message = "Usuario Cadastrado com sucesso!"


class UsuarioUpdateView(SuccessMessageMixin,UpdateView):
    model = Usuario
    form_class = UsuarioModelForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuarios')
    success_message = "Usuario Atualizado com sucesso!"

class UsuarioDeleteView(SuccessMessageMixin,DeleteView):
    model = Usuario
    template_name = 'usuarios_apagar.html'
    success_url = reverse_lazy('usuarios')
    success_message= "Usuario Deletado com sucesso!"
