from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_user_email_task(title, message, email=None):
    send_mail(
        title,
        message,
        email,
        ['eldosnursultan@gmail.com',
         'akylova.erkaiym@gmail.com',
         'aliaskar.isakov@gmail.com',
         'aktan.r.a@gmail.com',
         'alymbekovdastan1@gmail.com',
         'dinstamaly@gmail.com', ],
        fail_silently=False,
    )
    return True
