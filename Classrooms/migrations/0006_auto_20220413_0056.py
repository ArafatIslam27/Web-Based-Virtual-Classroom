# Generated by Django 3.2.4 on 2022-04-12 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Classrooms', '0005_alter_classroom_classroom_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='username',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='content',
        ),
    ]
