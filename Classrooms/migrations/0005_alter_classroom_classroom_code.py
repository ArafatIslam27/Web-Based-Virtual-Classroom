# Generated by Django 3.2.4 on 2022-04-09 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classrooms', '0004_auto_20220321_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='classroom_code',
            field=models.CharField(max_length=100),
        ),
    ]