# Generated by Django 3.2.4 on 2022-04-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classrooms', '0009_auto_20220428_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('S', 'Student'), ('T', 'Teacher')], max_length=200),
        ),
    ]
