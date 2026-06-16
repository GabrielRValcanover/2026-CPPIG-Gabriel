from datetime import timedelta, date

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from chaves.models import Chave
from .models import Emprestimo
from .models import EmprestimoCopiaChave
from reserva.models import Reserva
from .forms import EmprestimoModelForm, EmprestimoDevolucaoForm
from copia_chave.models import CopiaChave
from emprestimo.jobs import lembrete_email


class EmprestimoListView(PermissionRequiredMixin,ListView):
    permission_required = 'emprestimo.view_emprestimo'
    permission_denied_message = 'Visualizar emprestimo'
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
class EmprestimoAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'emprestimo.add_emprestimo'
    permission_denied_message = 'Cadastrar emprestimo'
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Cadastrado com sucesso!"
# regras de negocio de bloqueio por perda

    def form_valid(self, form):
        usuario = form.cleaned_data['pessoa']
        # chaves_pedida = Emprestimo.objects.filter( pessoa=usuario,copias_chave__status='perdida').distinct().count()
        # if chaves_pedida >= 3:
        #     form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 7 dias devido à perda de 3 chaves.')
        #     return self.form_invalid(form)
        # elif chaves_pedida >= 1:
        #     form.add_error( 'pessoa',f'{usuario.nome} você está bloqueado por 24 horas devido à perda de chave.')
        #     return self.form_invalid(form)
        if usuario.bloqueado_ate and usuario.bloqueado_ate >= date.today():
            form.add_error('pessoa', f'{usuario.nome} está bloqueado até {usuario.bloqueado_ate}.')
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

            reserva_ativa = Reserva.objects.filter(
                chaves=copia.chave,
                datahora_prevista__date=data,
                status__in=['pendente', 'confirmada']
            ).exists()

            if reserva_ativa:
                form.add_error( 'copias_chave',f'A chave "{copia}" possui reserva ativa para essa data!')
                return self.form_invalid(form)
# -----------------------------------------------------------------------------------------------------------------------------#
            # aqui faz a validação se é exclusiva ou cominitaria
            for ambiente in copia.chave.ambientes.all(): #
                if ambiente.exclusividade == 'exclusivas':
                    acessar = ambiente.acesso_permitido
                    if acessar != 'todos' and usuario.tipoUsuario != acessar:
                        form.add_error('copias_chave',f'Ambiente "{ambiente.nomenclatura}" é um ambiente esclusivo'
                                       f'para {ambiente.get_acesso_permitido_display()}')
                        return self.form_invalid(form)

 # https: // swesadiqul.medium.com / mastering - the - distinct - method - 12 d2cad2abda link que eu achei o significado do distinct() para nao entrar duplicado

            # if copia.chave.ambientes.count() == 1:
            #     precisa_chave_mestra = Chave.objects.filter(ambientes__in=copia.chave.ambientes.all()).distinct()
            #     for chave in precisa_chave_mestra:
            #         if chave.ambientes.count() > 1:
            #             if chave.copias.filter(status='emprestada').exists(): # coloquei essa verificação para ver se alguem ja tinha retirado a chave mestra
            #                 continue
            #             if not copias.filter(chave=chave).exists(): # precisa do not ( após quebrar a cabeça) para verificar se a chave precisa da mestra
            #                 form.add_error('copias_chave',' Essa chave precisa da mestra para acessar ao ambiente')
            #                 return self.form_invalid(form)

        for copia in copias:
            ambientes = copia.chave.ambientes.all()
            for ambiente in ambientes:
                bloco = ambiente.bloco
                if bloco:
                    # existe_mestra_no_bloco = Chave.objects.filter( ambientes__bloco=bloco,tipo='mestra' ).exists()
                    # if existe_mestra_no_bloco:
                    #     chave_mestra_selecionada = copias.filter(chave__tipo='mestra', chave__ambientes__bloco=bloco).exists()
                    #     if not chave_mestra_selecionada:
                    #         form.add_error('copias_chave',f'Para acessar o bloco {bloco.nome}, é necessário selecionar a chave mestra.')
                    #         return self.form_invalid(form)
                    existe_mestra_no_bloco = Chave.objects.filter(ambientes__bloco=bloco, tipo='mestraBloco').exists()
                    if existe_mestra_no_bloco:
                        mestra_ja_emprestada = CopiaChave.objects.filter(
                            chave__tipo='mestraBloco',
                            chave__ambientes__bloco=bloco,
                            status='emprestada'
                        ).exists()
                        if not mestra_ja_emprestada:
                            chave_mestra_selecionada = copias.filter(
                                chave__tipo='mestraBloco',
                                chave__ambientes__bloco=bloco
                            ).exists()
                            if not chave_mestra_selecionada:
                                form.add_error('copias_chave',
                                               f'Para acessar o bloco {bloco.nome}, é necessário selecionar a chave mestra.')
                                return self.form_invalid(form)

 # -----------------------------------------------------------------------------------------------------------------------------#

        # regra de quantidade de copias permitidas
        chaves_por_emprestimo = 0
        quantidade_chaves = Emprestimo.objects.filter(pessoa=usuario,data_devolucao__isnull=True)
        for emprestimo in quantidade_chaves:
                chaves_por_emprestimo += emprestimo.copias_chave.count()
        total_de_chaves = chaves_por_emprestimo + copias.count()
        if total_de_chaves > 5:
            form.add_error('pessoa',f'{usuario.nome} cota de 5 chaves excedita ')
            return self.form_invalid(form)

        # form.instance.status = 'emprestada'
        # response = super().form_valid(form)
        # lembrete_email(self.object) # função para mandar o email de 30 min
        # for copia in self.object.copias_chave.all():
        #     copia.status = 'emprestada'
        #     copia.save()
        # return response

        form.instance.status = 'emprestada'
        response = super().form_valid(form)
        for copia in copias:
            EmprestimoCopiaChave = object.create(emprestimo=self.object, copia_chave=copia)
            copia.status = 'emprestada'
            copia.save()
        lembrete_email(self.object)  # função para mandar o email de 30 min
        return response

class EmprestimoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'emprestimo.change_emprestimo'
    permission_denied_message = 'Edidar emprestimo'
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Atualizado com sucesso!"


class EmprestimoDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'emprestimo.delete_emprestimo'
    permission_denied_message = 'Ecluir emprestimo'
    model = Emprestimo
    template_name = 'emprestimos_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Emprestimo Deletado com sucesso!"

    def form_valid(self, form):
        for copia in self.object.copias_chave.all():
            copia.status = 'disponivel'
            copia.save()
        return super().form_valid(form)

#
# class EmprestimoDevolucaoView(SuccessMessageMixin, UpdateView):
#     model = Emprestimo
#     form_class = EmprestimoDevolucaoForm
#     template_name = 'emprestimo_devolucao.html'
#     success_url = reverse_lazy('emprestimos')
#     success_message = "Devolução registrada com sucesso!"
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         for copia in self.object.copias_chave.all():
#             verificacao_perdida = self.request.POST.get(f'verificacao_perdida_{copia.id}')
#             horario_devolucao = self.request.POST.get(f'horario_devolucao_{copia.id}')
#             if verificacao_perdida == 'perdida':
#                 usuario = self.object.pessoa
#                 mes = date.today() - timedelta(days=30)
#                 chaves_perdida = CopiaChave.objects.filter(
#                     emprestimos__pessoa=usuario,
#                     emprestimos__data_criacao__gte=mes,
#                     status='perdida'
#                 ).distinct().count()
#
#             # salva o status da copia
#             copia.status = verificacao_perdida
#             copia.horario_devolucao = horario_devolucao if horario_devolucao else None # usei o nome para não entrar "" e entrar none
#             copia.save()
#
#             # https://docs.djangoproject.com/en/6.0/topics/i18n/timezones/
#             # https://www.w3schools.com/django/ref_lookups_gte.php
#             if verificacao_perdida == 'perdida':
#                 if chaves_perdida >= 2:  # já tinha 2, agora com essa vira 3
#                     usuario.bloqueado_ate = date.today() + timedelta(days=7)
#                     usuario.save()
#                     messages.error(self.request, f'{usuario.nome} usuario bloqueado por 7 dias, após perder 3 chaves')
#                 else:  # 1ª ou 2ª perda
#                     usuario.bloqueado_ate = date.today() + timedelta(days=1)
#                     usuario.save()
#                     messages.error(self.request, f'{usuario.nome} usuario bloqueado por 24 horas, após perder chave')
#            #aqui faz a verificação se todas as chaves do emprestimo foram devolvidas
#             # todas_chaves_devolvidas = all(
#             # self.request.POST.get(f'verificacao_perdida_{copia.id}') in ['disponivel', 'perdida', 'danificada','manutencao']
#             #     for copia in self.object.copias_chave.all()
#             # )
#     todas_chaves_devolvidas = all(
#         copia.status in ['disponivel', 'perdida', 'danificada', 'manutencao']
#         for copia in self.object.copias_chave.all()
#     )
#
#     if todas_chaves_devolvidas:
#         self.object.status = 'devolvido'
#         ultima_copia = self.object.copias_chave.exclude(horario_devolucao__isnull=True).order_by('horario_devolucao').last()
#         if ultima_copia:
#             self.object.hora_devolucao = ultima_copia.horario_devolucao
#             self.object.data_devolucao = date.today()
#     else:
#         self.object.status = 'pendente'
#     self.object.save()
#     return response
        # todas_chaves_devolvidas = all(
        #     self.request.POST.get(f'verificacao_perdida_{copia.id}') in ['disponivel', 'perdida','danificada','manutencao']
        #     for copia in self.object.copias_chave.all()
        # )
        #
        # if todas_chaves_devolvidas:
        #     self.object.status = 'devolvido'  # usei pq é necessario para mudar o status na devolução da chave
        #     self.object.horario_devolucao = self.object.copias_chave.order_by('horario_devolucao').last().horario_devolucao # usei o last para ver o ultimo horario para
        #     self.object.save()
        #
        # return response
 #    def form_valid(self, form):
 #        response = super().form_valid(form)
 #        for copia in self.object.copias_chave.all():
 #            verificacao_perdida = self.request.POST.get(f'verificacao_perdida_{copia.id}')
 #            copia.status = verificacao_perdida
 #            copia.save()
 # #https: // docs.djangoproject.com / en / 6.0 / topics / i18n / timezones /  link do timedelta , usei o today para pegar a data de hoje e timedelta para ver a quantidade de duração
 # # https: // www.w3schools.com / django / ref_lookups_gte.php , onde eu li sobre o gte, para obter maiores ou iguias aos valores ( usei na data)
 #            if verificacao_perdida == 'perdida':
 #                usuario = self.object.pessoa
 #                mes = date.today() - timedelta(days=30)
 #                # chaves_pedida = Emprestimo.objects.filter(pessoa=usuario,data_devolucao__gte=mes,copias_chave__status='perdida').distinct().count()
 #                chaves_perdida = CopiaChave.objects.filter(emprestimos__pessoa=usuario,emprestimos__data_criacao__gte=mes,status = 'perdida').distinct().count()
 #                if chaves_perdida >= 3:
 #                    # usuario.bloqueado_ate = self.object.data_prevista
 #                   usuario.bloqueado_ate = date.today() + timedelta(days=7)
 #                   usuario.save()  # tive que salvar para conseguir visualizar os usuarios bloqueado
 #                   messages.error(self.request, f'{usuario.nome} usuario bloqueado por 7  dias, após perder 3 chave')
 #                elif chaves_perdida >= 1:
 #                    # usuario.bloqueado_ate = self.object.data_prevista assim dava erro
 #                    usuario.bloqueado_ate = date.today() + timedelta(days=1)
 #                    usuario.save()
 #                    messages.error(self.request, f'{usuario.nome} usuario bloqueado por 24 horas, após perder 1 chave')
 #        self.object.status = 'devolvido' # usei pq é necesario para mudar o status na devolução da chave
 #        self.object.save()
 #
 #        return response
class EmprestimoDevolucaoView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoDevolucaoForm
    template_name = 'emprestimo_devolucao.html'
    success_url = reverse_lazy('emprestimos')
    success_message = "Devolução registrada com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for copia in self.object.copias_chave.all():
            emprestmo_chave= EmprestimoCopiaChave.objects.filter(emprestimo=self.object, copia_chave=copia).first()
            if emprestmo_chave and emprestmo_chave.horario_devolucao:
                copia.horario_atual = emprestmo_chave.horario_devolucao.strftime('%H:%M')
            else:
                copia.horario_atual = ''
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        for copia in self.object.copias_chave.all():
            verificacao_perdida = self.request.POST.get(f'verificacao_perdida_{copia.id}')
            horario_devolucao = self.request.POST.get(f'horario_devolucao_{copia.id}')

            if verificacao_perdida == 'perdida':
                usuario = self.object.pessoa
                mes = date.today() - timedelta(days=30)
                chaves_perdida = CopiaChave.objects.filter(
                    emprestimos__pessoa=usuario,
                    emprestimos__data_criacao__gte=mes,
                    status='perdida'
                ).distinct().count()

            # salva o status da copia
            copia.status = verificacao_perdida
            # copia.horario_devolucao = horario_devolucao if horario_devolucao else None
            copia.save()

            if verificacao_perdida == 'perdida':
                if chaves_perdida >= 2:
                    usuario.bloqueado_ate = date.today() + timedelta(days=7)
                    usuario.save()
                    messages.error(self.request, f'{usuario.nome} usuario bloqueado por 7 dias, após perder 3 chaves')
                else:
                    usuario.bloqueado_ate = date.today() + timedelta(days=1)
                    usuario.save()
                    messages.error(self.request, f'{usuario.nome} usuario bloqueado por 24 horas, após perder chave')


        todas_chaves_devolvidas = all(
            copia.status in ['disponivel', 'perdida', 'danificada', 'manutencao']
            for copia in self.object.copias_chave.all()
        )

        # if todas_chaves_devolvidas:
        #     self.object.status = 'devolvido'
        #     ultima_copia = self.object.copias_chave.exclude(horario_devolucao__isnull=True).order_by('horario_devolucao').last()
        #     if ultima_copia:
        #         self.object.hora_devolucao = ultima_copia.horario_devolucao
        #         self.object.data_devolucao = date.today()
        # else:
        #     self.object.status = 'pendente'
        #
        # self.object.save()
        # return response

        if todas_chaves_devolvidas:
            self.object.status = 'devolvido'
            # ultima_copia = self.object.copias_chave.exclude(horario_devolucao__isnull=True).order_by('horario_devolucao').last()
            ultima_copia = EmprestimoCopiaChave.objects.filter(emprestimo=self.object, horario_devolucao__isnull=False).order_by('-horario_devolucao').first()
            if ultima_copia:
                self.object.hora_devolucao = ultima_copia.horario_devolucao
                self.object.data_devolucao = date.today()
        else:
            self.object.status = 'pendente'

        self.object.save()
        return response