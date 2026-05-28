
from datetime import datetime, timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

scheduler = BackgroundScheduler()

def lembrete_email(emprestimo):
    from emprestimo.utils.utils import lembrete
    datahora_prevista = datetime.combine(emprestimo.data_prevista,emprestimo.hora_prevista)
    horario_lembrete = datahora_prevista - timedelta(seconds=10)
    scheduler.add_job(
        lembrete,
        trigger='date',
        run_date=horario_lembrete,
        id=f'lembrete_{emprestimo.id}',
        replace_existing=True,
        args=[emprestimo.id],
    )

def aviso_atraso():
    print('JOB EXECUTANDO')
    from emprestimo.models import Emprestimo
    from emprestimo.utils.utils import chave_atrasada

    hoje = timezone.now()

    emprestimos = Emprestimo.objects.filter(status='emprestada',email_atraso=False)
    atrasados = []
    for emprestimo in emprestimos:
        datahora_prevista = datetime.combine(emprestimo.data_prevista,emprestimo.hora_prevista)
        datahora_prevista = timezone.make_aware(datahora_prevista)

        if datahora_prevista < hoje:
            atrasados.append(emprestimo)
            print(f'ENVIANDO EMAIL {emprestimo.id}')
            chave_atrasada(emprestimo.id)
            emprestimo.email_atraso = True
            emprestimo.save()
    print(atrasados)
def start():
    if scheduler.get_job('aviso_atraso') is None:
        scheduler.add_job(
            aviso_atraso,
            'interval',
            seconds=100,
            id='aviso_atraso'
        )
    if not scheduler.running:
        scheduler.start()
        print('SCHEDULER INICIADO')
