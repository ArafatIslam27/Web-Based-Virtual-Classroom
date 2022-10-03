from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import forms
from django.contrib.auth.forms import AuthenticationForm

app_name = "Classrooms"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("registration/login/", auth_views.LoginView.as_view(authentication_form=(forms.MyAuthenticationForm))),
    path("logout/", views.logout_request, name="logout"),
    path("account/", views.account_page, name="account_page"),
    path("Classrooms/", views.userpage, name="userpage"),
    path("Classrooms/<single_slug>/group_chat/", views.group_chat, name="group_chat"),
    path('Classrooms/<single_slug>/get_token/', views.getToken),
    path('Classrooms/<single_slug>/create_member/', views.createMember),
    path('Classrooms/<single_slug>/get_member/', views.getMember),
    path('Classrooms/<single_slug>/delete_member/', views.deleteMember),
    path("Classrooms/<single_slug>/video_room/", views.video_room, name="video_room"),
    path("Classrooms/<single_slug>/class_feed/", views.class_feed, name="class_feed"),
    path("api/<class_name>/announcement-list", views.AnnouncementList, name="announcement-list"),
    path("api/announcement-delete/<str:pk>", views.AnnouncementDelete, name="announcement-delete"),
    path("api/document-list", views.DocumentList, name="document-list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
