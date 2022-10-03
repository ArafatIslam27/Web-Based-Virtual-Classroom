from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Classroom(models.Model):
    room_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    teacher = models.CharField(max_length=200)
    student_count = models.IntegerField()
    classroom_slug = models.CharField(max_length=200, default=1)
    classroom_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.ForeignKey(Classroom, default=1, verbose_name="Room", on_delete=models.PROTECT)
    author=models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    content = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content

class Announcement(models.Model):
    author = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    def __str__(self):
        return self.content

class Document(models.Model):
    name = models.CharField(max_length=100)
    doc = models.FileField()
    rel_post = models.ForeignKey(Announcement, related_name='related_post', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=200, blank=True)
    uid = models.CharField(max_length=200, blank=True)
    room_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    USER_TYPE = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=200, choices=USER_TYPE, default='S')
    class_list = models.ManyToManyField(Classroom, blank=True)
    institutional_id = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user_type + ' user'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
