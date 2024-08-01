from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Mailing, MailingAttempt

@shared_task
def send_mailing_task(mailing_id):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        return

    if mailing.status == 'created' and mailing.start_date <= timezone.now():
        clients = mailing.clients.all()
        subject = mailing.message.subject
        body = mailing.message.body

        for client in clients:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [client.email],
                fail_silently=False,
            )

        mailing.status = 'completed'
        mailing.save()

        MailingAttempt.objects.create(
            mailing=mailing,
            status='Successful',
            response='Mailing sent successfully'
        )

@shared_task
def send_scheduled_mailings():
    from .tasks import send_mailing_task  # Импорт внутри функции
    mailings = Mailing.objects.filter(status='created', start_date__lte=timezone.now())
    for mailing in mailings:
        send_mailing_task.delay(mailing.id)
        mailing.status = 'started'
        mailing.save()

@shared_task
def start():
    from .tasks import send_mailing_task  # Импорт внутри функции
    current_datetime = timezone.now()
    mailings = Mailing.objects.filter(start_date__lte=current_datetime, status__in=['created', 'started'])

    for mailing in mailings:
        try:
            send_mailing_task.delay(mailing.id)
            mailing.status = 'started'
            mailing.save()

            MailingAttempt.objects.create(
                mailing=mailing,
                status='Successful',
                response='Mailing started'
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Failed',
                response=str(e)
            )
