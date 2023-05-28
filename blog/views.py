from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import signupform, loginform, Postform
from django.contrib.auth import authenticate, login, logout
from allauth.account.views import LogoutView

from django.contrib.auth.models import Group
from .models import Post

i=0
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def user_login(request):
    if request.method == 'POST':
        fm = loginform(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upassword = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                i=+1
                return HttpResponseRedirect('/dashboard/')
    else:
        fm = loginform()
    return render(request, 'blog/login.html', {'form': fm})


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': grps})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    logout_view = LogoutView.as_view()
    return logout_view(request, next_page='/')


def user_signup(request):
    if request.method == "POST":
        fm = signupform(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congratulation!! You have become an Author')
            user = fm.save()
            group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(group)

    else:
        fm = signupform()
    return render(request, 'blog/signup.html', {'form': fm})


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Postform(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                description = fm.cleaned_data['description']
                pst = Post(title=title, description=description)
                pst.save()
                fm = Postform()
        else:
            fm = Postform()
        return render(request, 'blog/addpost.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = Postform(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi = Post.objects.get(pk=id)
            fm = Postform(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')