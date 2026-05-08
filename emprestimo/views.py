from django.contrib import messages
from django.contrib.auth.models import User
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
        usuario = form.cleaned_data['pessoa']
        chaves_pedida = Emprestimo.objects.filter( pessoa=usuario,status='perdida').count()
        if chaves_pedida >= 3:
            form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 7 dias devido à perda de 3 chaves.')
            return self.form_invalid(form)

        elif chaves_pedida >= 1:
            form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 24 horas devido à perda de chave.')
            return self.form_invalid(form)

        copias = form.cleaned_data['copias_chave']
        data = form.cleaned_data['data_prevista']
        for copia in copias:

            if copia.status == 'emprestada':
                form.add_error('copias_chave',f'A cópia "{copia}" já está emprestada!')
                return self.form_invalid(form)

            reserva_ativa = Reserva.objects.filter(chaves=copia.chave,data_prevista=data,status__in=['pendente', 'confirmada']).exists()

            if reserva_ativa:
                form.add_error( 'copias_chave',f'A chave "{copia}" possui reserva ativa para essa data!')
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
        novo_status = form.cleaned_data['status']
        verificacao_perdida = form.cleaned_data['status']
        response = super().form_valid(form)
        for copia in self.object.copias_chave.all():
            copia.status = novo_status
            copia.save()

        if verificacao_perdida == 'perdida':
            usuario = self.object.pessoa
            chaves_pedida = Emprestimo.objects.filter(pessoa=usuario, status='perdida').count()
            if chaves_pedida >= 3:
                messages.error(self.request, f'{usuario.nome} usuario bloqueado por 7  dias após perder 3 chave')
            elif chaves_pedida >= 1:
                messages.error(self.request, f'{usuario.nome} usuario bloqueado por 24 horas após perder 1 chave')

        return response
