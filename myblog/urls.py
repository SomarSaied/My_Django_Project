"""miniblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.user_signup,name='sign_up'),
    path('login/',views.user_login,name='log_in'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.user_logout,name='log_out'),
    path('add/',views.add_post,name='add'),
    path('update/<int:id>/',views.update_post,name='update'),
    path('delete/<int:id>/',views.delete_post,name='delete'),
]
