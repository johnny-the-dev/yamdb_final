import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.filters.CharFilter(
        field_name='genre__slug',
    )
    category = django_filters.filters.CharFilter(
        field_name='category__slug',
    )
    name = django_filters.filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']
