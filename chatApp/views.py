import json
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Profile, Friend, Request, Message
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user.pk)
        
        #========================= Suggestion List =========================
        other_profiles = Profile.objects.exclude(user_id=profile.user.pk)
        exclude_list = other_profiles
        requested_list = Request.objects.filter(request_from=profile.pk)
        
        for requests in requested_list:
            pro = Profile.objects.get(pk=requests.request_to.pk)
            if pro in exclude_list:
                exclude_list = exclude_list.exclude(pk=pro.pk)
                
        friends_list = Friend.objects.filter(user=profile)
        
        for friend in friends_list:
            if friend.friend in exclude_list:
                exclude_list = exclude_list.exclude(pk=friend.friend.pk)
                
        suggestion_list = []
        for us in exclude_list:
            temp_dic = {'username': us.user.username, 'picture': us.picture}
            suggestion_list.append(temp_dic)
        
        context = {'profile': profile, 'suggestion_list': suggestion_list}
        
        return render(request, 'home.html', context)
    
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    user_form = SignUpForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password1"]
            
            user.save()
            profile.save()
            
            log_user = authenticate(username=username, password=password)
            auth_login(request, log_user)
            messages.success(request, "Registration success!")
            
            return redirect('home')
        
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})
    

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # messages.success(request, "Logged in successfully!")
            return redirect('home')
        
        else:
            messages.success(request, "There was an error. Please Login again!")
    
    return render(request, 'login.html', {})
    

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, "You have been logged out!")
    return redirect('home')


def chats_data(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        profile = Profile.objects.get(user=request.user.pk)
        
        #=========================== Request List ===========================
        friend_request_list = Request.objects.filter(request_to=profile.pk)
        friend_request_list = [Profile.objects.get(pk=friend_request.request_from.pk) for friend_request in friend_request_list]
        
        request_list = []
        for friend_request in friend_request_list:
            temp_dic = {'username': friend_request.user.username, 'picture': friend_request.picture.url}
            request_list.append(temp_dic)
        
        #=========================== Friends List ===========================
        friends_query = Friend.objects.filter(user=profile)
        
        friends_list = []
        for friend in friends_query:
            temp_dic = {"username": friend.friend.user.username, "picture": friend.friend.picture.url}
            
            last_message = Message.objects.filter( Q(sender=friend.friend, receiver=profile) | Q(sender=profile, receiver=friend.friend)).last()
            if last_message:
                if last_message.sender == friend.friend:
                    temp_dic["last_message"] = {"seen": last_message.seen, "message": last_message.body}  
                else:
                    temp_dic["last_message"] = { "message": last_message.body}  
                    
            
            friends_list.append(temp_dic)

        data = {"request_list": request_list, "friends_list": friends_list}
        return JsonResponse(data, safe=False)
    
    return JsonResponse({"request" : "Failed"}, safe=False)


def send_request(request, user):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        request_from = Profile.objects.get(user=request.user.pk)
        send_to_user = User.objects.get(username=user[:-7])
        request_to = Profile.objects.get(user=send_to_user.pk)
        
        new_request = Request(request_from=request_from, request_to=request_to)
        new_request.save()
        
        return JsonResponse({'request_sent': True}, safe=False)
    return JsonResponse({'request_sent': False}, safe=False)


def request_action(request, action):
    if request.headers.get('X-Requested-With') == "XMLHttpRequest":
        action, requester = action.split("_")
        
        user_profile = Profile.objects.get(user=request.user.pk)
        requester_user = User.objects.get(username=requester)
        requester_profile = Profile.objects.get(user=requester_user.pk)
        
        if action == 'accept':
            new_friend = Friend(user=user_profile, friend=requester_profile)
            new_friend.save()
            new_friend = Friend(user=requester_profile, friend=user_profile)
            new_friend.save()
            print('this', action, requester)
        
        Request.objects.get(request_to=user_profile, request_from=requester_profile).delete()
        Request.objects.get(request_to=requester_profile, request_from=user_profile).delete()
    
        return JsonResponse({'accepted': True}, safe=False)
    return JsonResponse({'accepted': False}, safe=False)


def get_convo(request, friend):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        user_profile = Profile.objects.get(user=request.user.pk)
        friend_user = User.objects.get(username=friend)
        friend_profile = Profile.objects.get(user=friend_user.pk)
        
        chats = Message.objects.filter(Q(sender=user_profile, receiver=friend_profile) | Q(sender=friend_profile, receiver=user_profile)).order_by("pk")
        
        received_chats = chats.filter(receiver=user_profile)
        received_chats.update(seen=True)
        
        if not chats:
            return JsonResponse(None, safe=False)
        
        data = []
        for chat in chats:
            tempdic = {"message": chat.body}
            tempdic["is_user"] = True if chat.sender == user_profile else False
            data.append(tempdic)
        
        print(data)
        return JsonResponse(data, safe=False)
            
    return JsonResponse({"Bypass": "Blocked"}, safe=False)


def send_message(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        friend = data["sent_to"]
        body = data["message"].strip().replace("\n", "<br>")
        
        user_profile = Profile.objects.get(user=request.user.pk)
        friend_user = User.objects.get(username=friend)
        friend_profile = Profile.objects.get(user=friend_user.pk)
        
        new_message = Message(sender=user_profile, receiver=friend_profile, body=data["message"])
        new_message.save()
        
        return JsonResponse(True, safe=False)
    
    return JsonResponse(False, safe=False)