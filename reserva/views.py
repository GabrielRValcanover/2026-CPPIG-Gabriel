from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator


from .models import Reserva
from .forms import ReservaModelForm




class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'reservas'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservaListView, self).get_queryset()
        if buscar:
            return qs.filter(pessoa__nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,10)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          messages.info(self.request,'Não existem Reservas cadastradas!')
        return qs


class ReservaAddView(SuccessMessageMixin, CreateView):
  model = Reserva
  form_class = ReservaModelForm
  template_name = 'reserva_form.html'
  success_url = reverse_lazy('reservas')
  success_message = 'Reserva cadastrada com sucesso!'

  def form_valid(self, form):
    form.instance.status = 'pendente'
    return super().form_valid(form)


class ReservaUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'


class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reservas_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva excluída com sucesso!'
