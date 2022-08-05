from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='Home'),
    path('result/<str:type>', Result, name='result'),
    path('adddata', AddData, name='add_data'),    
]