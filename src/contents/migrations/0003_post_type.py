# Generated by Django 5.2.1 on 2025-05-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('post', 'Пост'), ('good_morning', 'Доброе утро'), ('good_night', 'Спокойной ночи'), ('happy', 'Счасливый'), ('sad', 'Грустный')], default='post', help_text='Тип поста', verbose_name='Тип поста'),
        ),
    ]
