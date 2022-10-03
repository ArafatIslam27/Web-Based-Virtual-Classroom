from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Classroom, Message, Participant, Profile, Announcement, Document
from .forms import NewUserForm, ProfileForm, AddClassForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core import serializers
from .serializers import DocumentSerializer, AnnouncementSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json


@login_required
def userpage(request):
    if request.method == "POST":
        form = AddClassForm(request.POST)
        if form.is_valid():
            classroom_code = form.cleaned_data.get("classroom_code")
            class_list = [c.classroom_code for c in Classroom.objects.all()]
            class_list_user = [c.classroom_code for c in request.user.profile.class_list.all()]
            if classroom_code in class_list:
                if classroom_code in class_list_user:
                    messages.error(request, "You are already enrolled in this class!")
                else:
                    classroom = Classroom.objects.filter(classroom_code=classroom_code)[0]
                    request.user.profile.class_list.add(classroom)
                    cnt = classroom.student_count + 1
                    Classroom.objects.filter(classroom_code=classroom_code).update(student_count=cnt)
                    messages.success(request, f"You are added to {classroom.name} class")
                    return redirect("Classrooms:userpage")
            else:
                messages.error(request, "No such classroom code exists!")

    form = AddClassForm()
    return render(request=request,
           template_name="Classrooms/classrooms.html",
           context={"rooms": Classroom.objects.all,
                    "users": User.objects.all,
                    "user_profiles": Profile.objects.all,
                    "form":form,
            })

@login_required
def group_chat(request, single_slug):
    classrooms = [c.classroom_slug for c in Classroom.objects.all()]
    if single_slug in classrooms:
        return render(request=request,
               template_name="Classrooms/room.html",
               context={"room_name_json": mark_safe(json.dumps(single_slug)),
                        "username": mark_safe(json.dumps(request.user.username)),
                })
    else:
        return HttpResponse(f"{single_slug} is not a classroom that we know of")

def homepage(request):
    # form = AuthenticationForm(request=request, data=request.POST)
    return render(request=request,
           template_name="Classrooms/home.html",
           context={"classrooms": Classroom.objects.all})

def register(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        #inst_id = request.POST['institutional_id']
        #contact = request.POST['contact']
        #address = request.POST['address']
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data.get('username')
            #Profile.objects.filter(user__username=username).update(institutional_id=inst_id, contact=contact, address=address)
#            profile_form.save()

            messages.success(request, f"New account created: {username}")
            login(request, user)
#            p_t = profile_form.cleaned_data.get('user_type')
#            user.profile.user_type = p_t
#            setattr(request.user.profile, 'user_type', p_t)
            return redirect("Classrooms:userpage")
#            return render(request=request,
#                   template_name="Classrooms/classrooms.html",
#                   context={"rooms": Classroom.objects.all})
        else:
#            for msg in user_form.error_messages:
#                messages.error(request, f"{msg}: {user_form.error_messages[msg]}")
            for field, items in user_form.errors.items():
                for item in items:
                    messages.error(request, f"{field}: {item}")

    user_form = NewUserForm()
    profile_form = ProfileForm()
    return render(request=request,
           template_name="Classrooms/register.html",
           context={"user_form":user_form, "profile_form":profile_form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("Classrooms:userpage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request=request,
           template_name="Classrooms/login.html",
           context={"form":form})

@login_required
def account_page(request):
    user = request.user
    if request.method == 'POST':
        old_pass = request.POST['old-pass']
        new_pass = request.POST['new-pass']
        re_new_pass = request.POST['re-new-pass']
        if old_pass and user.check_password(old_pass):
            if new_pass and re_new_pass and new_pass == re_new_pass:
                user.set_password(new_pass)
                user.save()
                login(request, user)
                messages.info(request, "Changed password successfully")
                return redirect('Classrooms:account_page')
            else:
                messages.info(request, "New password and re-typed passwords do not match")
                return redirect('Classrooms:account_page')
        else:
            messages.info(request, "Current password is incorrect")
            return redirect('Classrooms:account_page')

    return render(request, "Classrooms/account.html", {})

@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Classrooms:homepage")

@login_required
def class_feed(request, single_slug):
    user = request.user
    class_name = Classroom.objects.filter(classroom_slug=single_slug)[0].name
    if request.method == 'POST':
        data = request.POST
        docs = request.FILES.getlist('docs')
        rel_post = Announcement.objects.create(
            author=user.username,
            class_name=class_name,
            content=data['content'],
        )
        for f in docs:
            docfile = Document.objects.create(
                name=f.name,
                doc=f,
                rel_post=rel_post,
            )
        return redirect('Classrooms:class_feed', single_slug)

    # Might need changes
    posts = Announcement.objects.filter(class_name=class_name)
    posts = posts.order_by('-timestamp')
#    docs = Document.objects.all()
#    serializer = DocumentSerializer(docs, many=True)
#    rel_posts = Document.objects.only('rel_post')
    context = {
        "posts": json.dumps([model_to_dict(x) for x in posts]),
        "class_name": mark_safe(json.dumps(class_name)),
        "roomName": mark_safe(json.dumps(single_slug)),
        "user_type": mark_safe(json.dumps(user.profile.user_type)),
#        "docs": serializer.data, #serializers.serialize("json", docs),
#        "rel_posts": json.dumps([model_to_dict(x) for x in rel_posts]),
    }
    return render(request=request,
                  template_name="Classrooms/class_feed.html",
                  context=context)

#class AnnouncementListView(generics.ListCreateAPIView):
#    serializer_class = AnnouncementSerializer
#    queryset = Announcement.objects.all()

#class DocumentListView(generics.ListCreateAPIView):
#    serializer_class = DocumentSerializer
#    queryset = Document.objects.all()

@api_view(['GET'])
def DocumentList(request):
    docs = Document.objects.all()
    serializer = DocumentSerializer(docs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def AnnouncementList(request, class_name):
    posts = Announcement.objects.filter(class_name=class_name)
    posts = posts.order_by('-timestamp')
    serializer = AnnouncementSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def AnnouncementDelete(request, pk):
    post = Announcement.objects.get(id=pk)
    post.delete()
    return Response('Post deleted successfully!')

@login_required
def video_room(request, single_slug):
#    if request.user.profile.user_type == 'S':
#        messages.error(request, "You are not allowed to start a video call!")
#    else:
    return render(request=request,
                  template_name="Classrooms/video_room.html",
                  context={"users": User.objects.all})

@login_required
def getToken(request, single_slug):
    appId = "4001f68773ff44e9a014bf192b241b7d"
    appCertificate = "9f1973c580c94efb9ec185181b2bef95"
    channelName = single_slug
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600*24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@login_required
@csrf_exempt
def createMember(request, single_slug):
    data = json.loads(request.body)

    member, created = Participant.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

@login_required
def getMember(request, single_slug):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = Participant.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@login_required
@csrf_exempt
def deleteMember(request, single_slug):
    data = json.loads(request.body)
    member = Participant.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

def get_last_10_messages(roomName):
    room = Classroom.objects.filter(classroom_slug=roomName)[0]
    room_messages = Message.objects.filter(room_name=room)
    return room_messages.order_by('-timestamp').all()[:10]
