from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('<str:username>', Home, name='home'),
    path('result/<str:username>/<str:link>', Result, name='result'),
    path('backend/',Backend,name='backend'),
    path('backend/<str:username>/listhuay',ListHuay,name='list_huay'),
    path('backend/listuser',ListUser,name='list_user'),
    path('backend/add/user',AddUser,name='add_user'),
    path('backend/edit/user/<str:username>',EditUser,name='edit_user'),
    path('backend/<str:username>/add/detailpic',AddHuay,name='add_huay'),
    path('backend/<str:username>/edit/detailpic/<int:huay_id>',EditHuay,name='edit_huay'),
]