from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User, post, Userprofile
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

class write(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'add-text', 'placeholder':'What are you thinking about?'}), label='')

def index(request):
    posts = post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'write': write,
        'page_obj':page_obj
    }
    return render(request, "network/index.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def following_posts(request):
    try:
        f = Userprofile.objects.get(user=request.user).following.all()
        posts = post.objects.filter(user__in=f)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'posts': posts,
            'page_obj':page_obj
        }
        return render(request, "network/following.html", context)
    except:
        pass
@login_required(login_url='/login')
def profile(request, username):
    if request.method == "POST":
        try:
            user = get_object_or_404(User, username=username)
            # removing user from current user following list if found
            current_user = Userprofile.objects.get(user=request.user, following=user)
            current_user.following.remove(user)

            # removing current user from user followers list if found
            profile_user = Userprofile.objects.get(user=user, follower=request.user)
            profile_user.follower.remove(request.user)
            return redirect('/')
        except:
            user = get_object_or_404(User, username=username)
            # adding user to current user following list
            current_user = Userprofile.objects.get(user=request.user)
            current_user.following.add(user)

            # adding current user to user followers list
            profile_user = Userprofile.objects.get(user=user)
            profile_user.follower.add(request.user)
            return redirect('/')

    else:
        user = get_object_or_404(User, username=username)
        user_posts= post.objects.filter(user=user).order_by('id').reverse()
        current_user = request.user
        profiles = Userprofile.objects.get(user=user)
        paginator = Paginator(user_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'user_posts':user_posts,
            'profile': profiles,
            'current_user':current_user,
            'user':user,
            'page_obj':page_obj
        }
        return render(request, "network/profile.html", context)


@login_required(login_url='/login')
def add_post(request):
    if request.method == "POST":
        form = write(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            post.objects.create(user=request.user,text=text)
            return redirect('index')
    else:
        context = {
            'write': write
        }
        return render(request, "network/create.html", context)

def edit_post(request, id):
    if request.method == "POST":
        posts = post.objects.get(id=id)
        form = write(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            posts.text = text
            posts.edited = True
            posts.save()
            return redirect('index')
    else:
        posts = post.objects.get(id=id)
        data = posts.text
        context = {
            'posts': posts,
            'write': write(initial={'text':data})
        }
        return render(request, "network/edit.html", context)

@login_required(login_url='/login')
def delete_post(request, id):
    if request.method == "POST":
        posts = post.objects.get(id=id)
        posts.delete()
        return redirect('index')
    else:
        posts = post.objects.get(id=id)
        context = {
            'posts': posts
        }
        return render(request, "network/delete.html", context)


@login_required(login_url='/login')
@csrf_exempt
def like(request):
    if request.method == 'GET':
        try:
            user = request.user
            id = request.GET['id']
            posts = post.objects.get(id=id)
            if user in posts.likes.all():
                posts.likes.remove(user)
            else:
                posts.likes.add(user)
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({'error':'error'}, status=400)
