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

# https://docs.djangoproject.com/en/6.0/ref/forms/api/#django.forms. Form.add_error  || fonte do Form.add_erro onde eu encontrei
class EmprestimoAddView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Cadastrado com sucesso!"
# regras de negocio de bloqueio por perda

    def form_valid(self, form):
        usuario = form.cleaned_data['pessoa']
        chaves_pedida = Emprestimo.objects.filter( pessoa=usuario,copias_chave__status='perdida').distinct().count()
        if chaves_pedida >= 3:
            form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 7 dias devido à perda de 3 chaves.')
            return self.form_invalid(form)
        elif chaves_pedida >= 1:
            form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 24 horas devido à perda de chave.')
            return self.form_invalid(form)

#-----------------------------------------------------------------------------------------------------------------------------#
        copias = form.cleaned_data['copias_chave']
        data = form.cleaned_data['data_prevista']
        for copia in copias:
            if copia.status == 'emprestada':
                form.add_error('copias_chave',f'A cópia "{copia}" já está emprestada!')
                return self.form_invalid(form)

            if copia.status == 'perdida':
                form.add_error('copias_chave', f'A cópia"{copia}" foi PERDIDA!! entre em contato com a direção')
                return self.form_invalid(form)

            reserva_ativa = Reserva.objects.filter(chaves=copia.chave,data_prevista=data,status__in=['pendente', 'confirmada']).exists()

            if reserva_ativa:
                form.add_error( 'copias_chave',f'A chave "{copia}" possui reserva ativa para essa data!')
                return self.form_invalid(form)

 # https: // swesadiqul.medium.com / mastering - the - distinct - method - 12 d2cad2abda link que eu achei o significado do distinct() para nao entrar duplicado

            if copia.chave.ambientes.count() == 1:
                precisa_chave_mestra = Chave.objects.filter(ambientes__in=copia.chave.ambientes.all()).distinct()
                for chave in precisa_chave_mestra:
                    if chave.ambientes.count() > 1:
                        if chave.copias.filter(status='emprestada').exists(): # coloquei essa verificação para ver se alguem ja tinha retirado a chave mestra
                            continue
                        if not copias.filter(chave=chave).exists(): # precisa do not ( após quebrar a cabeça) para verificar se a chave precisa da mestra
                            form.add_error('copias_chave',' Essa chave precisa da mestra para acessar ao ambiente')
                            return self.form_invalid(form)

# regra de quantidade de copias permitidas
        chaves_por_emprestimo = 0
        quantidade_chaves = Emprestimo.objects.filter(pessoa=usuario,data_devolucao__isnull=True)
        for emprestimo in quantidade_chaves:
                chaves_por_emprestimo += emprestimo.copias_chave.count()
        total_de_chaves = chaves_por_emprestimo + copias.count()
        if total_de_chaves > 5:
            form.add_error('pessoa',f'{usuario.nome} cota de chaves excedita ')
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
        response = super().form_valid(form)
        for copia in self.object.copias_chave.all():
            verificacao_perdida = self.request.POST.get(f'verificacao_perdida_{copia.id}')
            print(f'copia {copia.id} -> {verificacao_perdida}')
            copia.status = verificacao_perdida
            copia.save()

            if verificacao_perdida == 'perdida':
                usuario = self.object.pessoa
                chaves_pedida = Emprestimo.objects.filter(pessoa=usuario, status='perdida').count()
                if chaves_pedida >= 3:
                   usuario.bloqueado_ate = self.object.data_prevista
                   usuario.save()  # tive que salvar para conseguir visualizar os usuarios bloqueado
                   messages.error(self.request, f'{usuario.nome} usuario bloqueado por 7  dias, após perder 3 chave')
                elif chaves_pedida >= 1:
                   usuario.bloqueado_ate = self.object.data_prevista
                   usuario.save()
                   messages.error(self.request, f'{usuario.nome} usuario bloqueado por 24 horas, após perder 1 chave')
        self.object.status = 'devolvido' # usei pq é necesario para mudar o status na devolução da chave
        self.object.save()

        return response
