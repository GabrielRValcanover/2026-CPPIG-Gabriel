from datetime import date

from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin

from .utils.utils import adiciona_job
from .models import Reserva
from .forms import ReservaModelForm

class ReservaListView(PermissionRequiredMixin,ListView):
    permission_required = 'reserva.view_reserva'
    permission_denied_message = 'Visualizar reserva'
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'reservas'

#https://docs.djangoproject.com/en/6.0/topics/i18n/timezones/ link do now w today()
#https: // academify.com.br / datas - e - horas - no - python - com - datetime /
    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservaListView, self).get_queryset()
        if buscar:
            qs = qs.filter(pessoa__nome__icontains=buscar)

        if qs.count() == 0:
            messages.info(self.request, 'Não existem Reservas cadastradas!')

        paginator = Paginator(qs, 6)
        listagem = paginator.get_page(self.request.GET.get('page'))
        return listagem


class ReservaAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
  permission_required = 'reserva.add_reserva'
  permission_denied_message = 'Cadastrar reserva'
  model = Reserva
  form_class = ReservaModelForm
  template_name = 'reserva_form.html'
  success_url = reverse_lazy('reservas')
  success_message = 'Reserva cadastrada com sucesso!'

  def form_valid(self, form):
    form.instance.status = 'pendente'
    response = super().form_valid(form)
    adiciona_job(self.object)
    return response


class ReservaUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'reserva.change_reserva'
    permission_denied_message = 'Editar reservva'
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'


class ReservaDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'reserva.delete_reserva'
    peRmission_denied_message = 'Excluir reservva'
    model = Reserva
    template_name = 'reservas_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva excluída com sucesso!'
