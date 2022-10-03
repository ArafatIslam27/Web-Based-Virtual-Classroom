from django.contrib import admin
from .models import Classroom, Message, Participant, Profile, Announcement, Document

# Register your models here.
admin.site.register(Classroom)
admin.site.register(Message)
admin.site.register(Participant)
admin.site.register(Profile)
admin.site.register(Announcement)
admin.site.register(Document)
