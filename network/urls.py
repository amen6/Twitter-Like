from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile , name="profile"),
    path("newpost", views.add_post, name="addpost"),
    path("followingPosts", views.following_posts, name="following"),
    path("edit/<str:id>", views.edit_post, name="edit"),
    path("delete/<str:id>", views.delete_post, name="delete"),
    url(r'^like/$', views.like, name="like")
]
