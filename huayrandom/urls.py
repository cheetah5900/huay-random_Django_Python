from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('<str:username>', Home, name='home'),
    path('result/<str:username>/<str:link>', Result, name='result'),
    path('backend/',Backend,name='backend'),
    path('backend/<str:username>/listhuay',ListHuay,name='list_huay'),
    path('backend/<str:username>/add/detailpic',AddDetailPicture,name='add_detail_picture'),
    path('backend/<str:username>/edit/detailpic/<int:huay_id>',EditDetailPicture,name='edit_detail_picture'),
]