
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import UsuarioModelForm
from .models import Usuario
from datetime import date
from django.views.generic import ListView


class UsuariosListView(ListView):
    model = Usuario
    template_name = 'usuarios.html'

    def get_context_data(self, **kwargs):
        contador = super().get_context_data(**kwargs)
        # usuarios_bloqueados = []   # coloco os usuarios em uma lista para contar
        # for usuario in Usuario.objects.all():
        #     if usuario.bloqueado_ate:
        #         usuarios_bloqueados.append(usuario)  # uso o append para  por um incone no final da lista
        # contador['usuarios_bloqueados'] = len(usuarios_bloqueados)
        contador['usuarios_bloqueados'] = Usuario.objects.filter(bloqueado_ate__gte=date.today()).count()
        return contador

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(UsuariosListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,10)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
            messages.info(self.request,'Não existem usuarios cadastrados!')
        return qs

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

#
# class UsuariosBloqueadosListView(ListView):
#     model = Usuario
#     template_name = 'usuarios_bloqueados.html'
#
#     def get_queryset(self, **kwargs):
#         return Usuario.objects.filter(bloqueado_ate__gte=date.today())
#         # usuarios_bloqueados = []
#         # for usuario in Usuario.objects.all():
#         #     if usuario.bloqueado_ate:
        #         usuarios_bloqueados.append(usuario)
        # return usuarios_bloqueados


class UsuariosBloqueadosListView(ListView):
    model = Usuario
    template_name = 'usuarios_bloqueados.html'

    def get_queryset(self):
        queryset = Usuario.objects.filter( bloqueado_ate__gte=date.today())
        buscar = self.request.GET.get('buscar')
        if buscar: queryset = queryset.filter(nome__icontains=buscar)
        return queryset