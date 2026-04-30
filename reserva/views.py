from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from pyexpat.errors import messages
from django.core.paginator import Paginator


from .models import Reserva
from .forms import ReservaModelForm




class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservaListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count()>0:
          paginator = Paginator(qs,2)
          listagem = paginator.get_page(self.request.GET.get('page'))
          return listagem
        else:
          return messages.info(self.request,'Não existem Reservas cadastradas!')


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
    template_name = 'reserva_confirm_delete.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva excluída com sucesso!'