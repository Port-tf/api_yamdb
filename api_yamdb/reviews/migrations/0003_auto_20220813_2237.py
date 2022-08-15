# Generated by Django 2.2.16 on 2022-08-13 19:37

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('reviews', '0002_auto_20220810_1531'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Titles',
            new_name='Title',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_author_title'),
        ),
    ]