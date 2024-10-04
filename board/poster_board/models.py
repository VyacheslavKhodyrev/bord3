from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None, verbose_name="Автор")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    title = models.CharField(max_length=128, verbose_name='Название')
    text = models.TextField(verbose_name='Oписание', blank=True, null=True)
    media = models.FileField(upload_to='media/%Y/%m/%d/', blank=True, null=True, verbose_name="Файл")

    def __str__(self):
        return f'{self.title}: {self.text}'

    class Meta:
        verbose_name = 'Oбъявлениe'
        verbose_name_plural = 'Oбъявления'
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


class Category(models.Model):
    CATEGORY = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('damage_dealers', 'ДД'),
        ('dealers', 'Торговцы'),
        ('gildmasters', 'Гилдмастеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY, unique=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post.title}: {self.text}'

    def get_absolute_url(self):
        return f'/posts/{self.post.pk}/comments/'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']
