from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from chaves.models import Chave
from .models import Emprestimo
from reserva.models import Reserva
from .forms import EmprestimoModelForm, EmprestimoDevolucaoForm


class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(EmprestimoListView, self).get_queryset()
        if buscar:
            return qs.filter(pessoa__nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem empréstimos cadastrados!')
            return qs


class EmprestimoAddView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Cadastrado com sucesso!"

    def form_valid(self, form):
      copias = form.cleaned_data['copias_chave']
      data = form.cleaned_data['data_prevista']

      for copia in copias:
        if copia.status == 'emprestada':
          form.add_error('copias_chave', f'A cópia "{copia}" já está emprestada!')
          return self.form_invalid(form)

        reserva_ativa = Reserva.objects.filter(chaves=copia.chave, data_prevista=data,status__in=['pendente', 'confirmada']).exists()
        if reserva_ativa:
          form.add_error('copias_chave', f'A chave "{copia}" possui reserva ativa para essa data!')
          return self.form_invalid(form)

        for ambiente in copia.chave.ambientes.all():
          if ambiente.bloco:
            chave_mestra = Chave.objects.filter(ambientes__bloco=ambiente.bloco, tipo='mestra').first()
            if chave_mestra:
              form.add_error('copias_chave', f'Para acessar {ambiente.nomenclatura} pegue também a chave mestra: {chave_mestra.descricao}')
              return self.form_invalid(form)

      form.instance.status = 'emprestada'
      response = super().form_valid(form)

      for copia in self.object.copias_chave.all():
        copia.status = 'emprestada'
        copia.save()

      return response

class EmprestimoUpdateView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Atualizado com sucesso!"


class EmprestimoDeleteView(SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimos_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Deletado com sucesso!"

    def form_valid(self, form):
      for copia in self.object.copias_chave.all():
        copia.status = 'disponivel'
        copia.save()
      return super().form_valid(form)


class EmprestimoDevolucaoView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoDevolucaoForm
    template_name = 'emprestimo_devolucao.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Devolução registrada com sucesso!"

    def form_valid(self, form):
        form.instance.status = 'devolvida'
        response = super().form_valid(form)
        for copia in self.object.copias_chave.all():
            copia.status = 'disponivel'
            copia.save()
        return response
