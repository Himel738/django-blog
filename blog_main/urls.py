"""
URL configuration for blog_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

import blogs
from . import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as BlogsView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path('category/', include('blogs.urls')),
    path('blogs/<slug:slug>/', BlogsView.blogs, name='blogs'),
    path('search/', BlogsView.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='forgot_password'),
    path('password-reset-sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Dashboard URLs
    path('dashboard/', include('dashboards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
