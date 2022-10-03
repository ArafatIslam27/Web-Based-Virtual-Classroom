# Generated by Django 3.2.4 on 2022-03-21 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Classrooms', '0003_auto_20220128_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='classroom_code',
            field=models.CharField(default='temp123', max_length=100),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('S', 'Student'), ('T', 'Teacher')], max_length=1)),
                ('class_list', models.ManyToManyField(blank=True, to='Classrooms.Classroom')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
