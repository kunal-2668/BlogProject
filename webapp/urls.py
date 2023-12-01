from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('login',loginView,name='login'),
    path('signup',signupView,name='signup'),
    path('logoutUser',logoutView,name='logout'),
    path('readmore/<str:slug>',readMore,name='readmore'),
    path('commentlike/<str:slug>/<int:id>',add_remove_comment_like,name='commentlike'),
    path('deleteComment/<str:slug>/<int:id>',deleteComment,name='deletecomment'),
    path('addcomment',addComment,name='addcomment'),
    path('search',Search,name='search'),
    path('addlike/<str:slug>',add_remove_blog_like,name='addlike'),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
