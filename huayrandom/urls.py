from django.urls import path
from huayrandom.views import *

urlpatterns = [
    path('', Index, name='index'),

    path('<str:username>', Home, name='home'),
    path('result/<str:username>/<str:link>', Result, name='result'),

    path('backend/', Backend, name='backend'),

    path('backend/huay/list',
         ListHuay, name='list_huay'),
    path('backend/huay/add',
         AddHuayList, name='add_huay_list'),
    path('backend/huay/edit/<int:id>',
         EditHuayList, name='edit_huay_list'),

    path('backend/huay/type/list/<str:username>',
         ListHuayType, name='list_huay_type'),
    path('backend/huay/type/add/<str:username>',
         AddHuayType, name='add_huay_type'),
    path('backend/huay/type/edit<str:username>/<int:huay_id>',
         EditHuayType, name='edit_huay'),

    path('backend/user/list', ListUser, name='list_user'),
    path('backend/user/add', AddUser, name='add_user'),
    path('backend/user/edit/<str:username>', EditUser, name='edit_user'),

]
