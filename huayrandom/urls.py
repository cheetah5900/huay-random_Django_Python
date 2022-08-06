from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('<str:username>', Home, name='home'),
    path('result/<str:username>/<str:link>', Result, name='result'),
    path('adddata', AddData, name='add_data'),    
    path('backend/',Backend,name='backend'),
    path('backend/<str:username>/add/detailpic',AddDetailPicture,name='add_detail_picture'),
]