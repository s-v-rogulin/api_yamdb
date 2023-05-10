import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

DB_TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Загрузка тестовых данных'

    def handle(self, *args, **kwargs):
        for model, csv_file in DB_TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                encoding='utf-8',
            ) as file:
                self.stdout.write(
                    self.style.HTTP_INFO(f'Файл: {csv_file}')
                )
                total = 0
                accepted = 0
                for data in csv.DictReader(file):
                    total += 1
                    if 'category' in data:
                        data['category'] = Category(data['category'])
                    if 'author' in data:
                        data['author'] = User(data['author'])
                    try:
                        res = model.objects.get_or_create(**data)
                    except IntegrityError:
                        ...
                    accepted += res[1]
                self.stdout.write(
                    self.style.MIGRATE_HEADING(f'Всего записей: {total}')
                )
                self.stdout.write(
                    self.style.HTTP_REDIRECT(f'Загружено: {accepted}')
                )
                print('-' * 40)
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
