from django.urls import path
from .views import ConfirmUser, ProfileUser

urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm'),
    path('profile/', ProfileUser.as_view(), name='profile'),
]
