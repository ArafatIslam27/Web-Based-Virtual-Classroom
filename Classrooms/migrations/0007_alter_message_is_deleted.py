# Generated by Django 3.2.4 on 2022-04-12 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classrooms', '0006_auto_20220413_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
