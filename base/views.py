import imp
from multiprocessing import context
from tkinter import EW
from unicodedata import name
from urllib import request
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name': "Let's learn Python."},
#     {'id': 2, 'name': "Design with me."},
#     {'id': 3, 'name': "Web Development"},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, "You are not exist.")

        user = authenticate(request, email=email, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "email and password not exist.")
            

    return render(request, 'base/login_register.html', {'page':page})

def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured registration.")

    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    room_participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context = {'room': room, 'room_messages':room_messages, 'room_participants':room_participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

def EditMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    
    
    if request.method == 'POST':
        message = Message.body(request.POST, instance = message)
        if message.body == request.POST.get('body'):
            if message.is_valid():
                message.save()
                return redirect('room', pk=room.id)

        
        
    context = {'message':message}
    return render(request, 'base/room.html', context)





@login_required(login_url='login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})

login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form':form})

def TopicsPages(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def ActivityPages(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})