from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

from  .models import Room,Topic,Message,User
from .forms import RoomForm,UserModel,myCreationForm
from django.db.models import Q
from django.contrib import messages
# from django.contrib.auth.models import User

def loginPage(request):
    page ='login'

    if request.user.is_authenticated:
       return redirect('home')
  
    if request.method== 'POST':
    #  username=request.POST.get('username').lower()
     email=request.POST.get('email')
     password=request.POST.get('password')
    
     try:
        user=User.objects.get(email=email)
        
     except:
        messages.error(request,'username does not exist') 
           
    
    
     user=authenticate(request,email=email,password=password)
     if user is not None:
      login(request,user)
      return redirect('home')
     else:
         
        messages.error(request,'username or password does not exist')
     
    context={'page':page}
    return render(request,'base/register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # form = UserCreationForm()
    form = myCreationForm()

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = myCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request,'base/register.html',{'form':form}) 

def home(request):
    q=request.GET.get('q')  if request.GET.get('q')!= None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                               Q(Q(name__icontains=q))|
                               Q(Q(descriptions__icontains=q))             
                              ) 
    topics=Topic.objects.all()[0:5]
    room_count=Room.objects.filter(Q(topic__name__icontains=q) |
                               Q(Q(name__icontains=q))|
                               Q(Q(descriptions__icontains=q))
                              
                              ).count()
    
    

    recent_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'recent_message':recent_message}
    return render(request,'base/home.html',context)

def room(request,pk):
    
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    
            
            
        
    context=  {'room':room,'room_messages':room_messages,'participants':participants}    
    return render(request,'base/room.html',context )


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
   
      topic_name=request.POST.get('topic')
      topic,created=Topic.objects.get_or_create(name=topic_name)
      Room.objects.create(
        host=request.user,
        topic=topic,
        name=request.POST.get('name'),
        descriptions=request.POST.get('descriptions'),
    
    )
      return redirect('home')
    
    # form = RoomForm()
    # if request.method=='POST':
    #     form=RoomForm(request.POST)
      
    #     form.is_valid()
    #     room=form.save(commit=False)
    #     room.host=request.user
    #     room.save()
        
        
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateForm(request,pk):
    topics=Topic.objects.all()
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
  
    
    
    if request.user!=room.host:
        return HttpResponse("you are not allowed")
    if request.method=='POST':
        # form=RoomForm(request.POST,instance=room) 
      topic_name=request.POST.get('topic')
      topic,created=Topic.objects.get_or_create(name=topic_name)
      room.name=request.POST.get('name')
      room.descriptions=request.POST.get('descriptions')
      room.topic=topic
      room.save()
      
    
        # if form.is_valid:
        #     form.save()
      return redirect('home')
 
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user!=room.host:
        return HttpResponse("you are not allowed")
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete_form.html', {'obj':room})
  
@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
  
    if request.user!=message.user:
        return HttpResponse("you are not allowed")
    
    if request.method=='POST':
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete_form.html', {'obj':message})
        
        
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    recent_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'recent_message':recent_message,'topics':topics}
    return render(request,'base/profile.html',context)       
        
@login_required(login_url='login')       
def updateUser(request):
    user=request.user
    form=UserModel(instance=user)
    if request.method=='POST':
        form=UserModel(request.POST,request.FILES, instance=user)
        if form.is_valid():
          form.save()
          return redirect('profile',pk=user.id)
    
      
    return render(request,'base/update_user.html',{'form':form})   

def topicPage(request):
   
    q=request.GET.get('q')  if request.GET.get('q')!= None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    recent_message=Message.objects.all()
    return render(request,'base/activity.html',{'recent_message':recent_message})