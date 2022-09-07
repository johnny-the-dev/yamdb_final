import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

FOLDER_PATH = 'static/data/'
FILENAMES = {
    'Category': 'category.csv',
    'Genre': 'genre.csv',
    'Title': 'titles.csv',
    'Genre_Title': 'genre_title.csv',
    'User': 'users.csv',
    'Review': 'review.csv',
    'Comments': 'comments.csv',
}


class Command(BaseCommand):
    '''
    Команда для наполнения БД из терминала.
    python3 manage.py load_db_from_static_data
    '''
    help = 'Наполнить БД данными из csv файлов в папке static/data'

    def populate_db(self, filename, loader_function):
        with open(FOLDER_PATH + filename, 'rt') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            for row in reader:
                loader_function(row)

    def load_categories(self, row):
        Category.objects.update_or_create(
            id=row[0],
            defaults={
                'name': row[1],
                'slug': row[2]
            }
        )

    def load_genres(self, row):
        Genre.objects.update_or_create(
            id=row[0],
            defaults={
                'name': row[1],
                'slug': row[2]
            }
        )

    def load_titles(self, row):
        Title.objects.update_or_create(
            id=row[0],
            defaults={
                'name': row[1],
                'year': row[2],
                'category': Category.objects.get(pk=row[3])
            }
        )

    def load_genre_title(self, row):
        title = Title.objects.get(pk=row[1])
        genre = Genre.objects.get(pk=row[2])
        title.genre.add(genre)

    def load_users(self, row):
        User.objects.update_or_create(
            id=row[0],
            defaults={
                'username': row[1],
                'email': row[2],
                'role': row[3],
                'bio': row[4],
                'first_name': row[5],
                'last_name': row[6]
            }
        )

    def load_reviews(self, row):
        title = Title.objects.get(pk=row[1])
        author = User.objects.get(pk=row[3])
        pub_date = datetime.strptime(
            row[5][:row[5].find('.')],
            '%Y-%m-%dT%H:%M:%S'
        )
        Review.objects.update_or_create(
            id=row[0],
            defaults={
                'title': title,
                'text': row[2],
                'author': author,
                'score': row[4],
                'pub_date': pub_date
            }
        )

    def load_comments(self, row):
        review = Review.objects.get(pk=row[1])
        author = User.objects.get(pk=row[3])
        pub_date = datetime.strptime(
            row[4][:row[4].find('.')],
            '%Y-%m-%dT%H:%M:%S'
        )
        Comment.objects.update_or_create(
            id=row[0],
            defaults={
                'review': review,
                'text': row[2],
                'author': author,
                'pub_date': pub_date
            }
        )

    def handle(self, *args, **kwargs):
        self.populate_db(FILENAMES['Category'], self.load_categories)
        print('--- loaded categories')
        self.populate_db(FILENAMES['Genre'], self.load_genres)
        print('--- loaded genres')
        self.populate_db(FILENAMES['Title'], self.load_titles)
        print('--- loaded titles')
        self.populate_db(FILENAMES['Genre_Title'], self.load_genre_title)
        print('--- loaded genre_title')
        self.populate_db(FILENAMES['User'], self.load_users)
        print('--- loaded users')
        self.populate_db(FILENAMES['Review'], self.load_reviews)
        print('--- loaded reviews')
        self.populate_db(FILENAMES['Comments'], self.load_comments)
        print('--- loaded comments')
