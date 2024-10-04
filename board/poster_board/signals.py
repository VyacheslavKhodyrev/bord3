from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from poster_board.models import *


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    if created:
        mail = instance.post.author.email
        send_mail(
            subject='Комментарий на объявление',
            message=f'На ваше ьобъявление {instance.post} пришел комментарий от {instance.author}',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )


@receiver(post_save, sender=Comment)
def accept_comment(sender, instance, created, **kwargs):
    if not created and instance.status:
        mail = instance.author.email
        send_mail(
            subject='Комментарий принят автором объявления',
            message=f'Ваш комментарий на {instance.post} принят автором. Спасибо за Ваш комментарий!',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )
