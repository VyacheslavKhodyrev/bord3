from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignUpForm, ProfileUserForm
from .models import OneTimeCode


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/registration/login'
    template_name = 'registration/signup.html'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST['code']
            one_time_code = OneTimeCode.objects.get(code=code)
            user = one_time_code.user
            if user:
                user.is_active = True
                user.save()
                one_time_code.delete()
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('account_login')

    def get(self, request):
        user = get_user_model()
        if request.user.is_authenticated:
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


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'accounts/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user
