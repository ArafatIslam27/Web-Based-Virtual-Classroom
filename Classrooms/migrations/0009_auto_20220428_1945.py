# Generated by Django 3.2.4 on 2022-04-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classrooms', '0008_rename_room_id_message_room_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='room_id',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='user_id',
        ),
        migrations.AddField(
            model_name='participant',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='participant',
            name='room_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='participant',
            name='uid',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='participant',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]