import email
from datetime import timezone, timedelta

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings


def lembrete(emprestimo_id):
    from emprestimo.models import Emprestimo

    try:

        emprestimo = Emprestimo.objects.get(id=emprestimo_id,status='emprestada')
        usuario = emprestimo.pessoa
        if not usuario.email:
            return
        if usuario.tipoUsuario == 'professor':
            tipo_lembrete = '1 dia'
        else:
            tipo_lembrete = '30 minutos'

        dados = {
            'usuario': usuario,
            'hora_prevista': emprestimo.hora_prevista,
            'tempo_aviso': tipo_lembrete,
        }
        texto_email = render_to_string( 'emails/texto_email.txt',dados )
        html_email = render_to_string('emails/texto_email.html',dados)

        emails = [
            usuario.email,
            'secretaria@projetoI.com.br',
            'inspetor@projetoI.com.br'
        ]
        send_mail(
            subject='E.E.E.F Maria Lucia - Lembrete',
            message=texto_email,
            from_email='gabrielvalcanover@gmail.com',
            recipient_list=emails,
            html_message=html_email,
            fail_silently=False,
        )
        print(f'Email enviado para {usuario.nome}')

    except Emprestimo.DoesNotExist:

        print('Emprestimo não encontrado')


def chave_atrasada(emprestimo_id):
    from emprestimo.models import Emprestimo

    try:
        emprestimo = Emprestimo.objects.get(id=emprestimo_id,status='emprestada')
        usuario = emprestimo.pessoa
        if not usuario.email:
            return
        dados = {
            'usuario': usuario,
            'data_prevista': emprestimo.data_prevista,
            'hora_prevista': emprestimo.hora_prevista,
        }

        texto_email = render_to_string('emails/texto_atraso_email.txt',dados)
        html_email = render_to_string('emails/texto_atraso_email.html',dados)

        emails = [
            usuario.email,
            'secretaria@projetoI.com.br',
            'inspetor@projetoI.com.br'
        ]

        send_mail(
            subject='E.E.E.F Maria Lucia - Chave em atraso',
            message=texto_email,
            from_email='gabrielvalcanover@gmail.com',
            recipient_list=emails,
            html_message=html_email,
            fail_silently=False,
        )
        print(f'Email de atraso enviado para {usuario.nome}')

    except Emprestimo.DoesNotExist:

        print('Emprestimo não encontrado')