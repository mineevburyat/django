# Generated by Django 4.1.4 on 2023-03-11 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libcatalog', '0004_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Отметить как возвращенный'),), 'verbose_name': 'Экземпляр книги', 'verbose_name_plural': 'Экземпляры книг'},
        ),
    ]
