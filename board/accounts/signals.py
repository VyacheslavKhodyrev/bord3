from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from poster_board.models import *


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    user = User.objects.get(id=instance.id)
    if created:
        subject = 'Добро пожаловать в MMORPG poster board!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/posts">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
    return user


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
