import django_filters
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import *
from django.forms import DateInput


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='iregex',
        label='Название содержит'
    )

    time_create = DateFilter(
        lookup_expr='date__gte',
        label='Дата позднее',
        widget=DateInput(
            format='%d.%m.%Y',
            attrs={'type': 'date'}
        )
    )

    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        lookup_expr='iregex',
        label='Категория',
        empty_label='Все категории'
    )


class CommentFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(CommentFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])
        self.filters['post'].label = 'Поиск по объявлению'

    class Meta:
        model = Comment
        fields = ('post',)
