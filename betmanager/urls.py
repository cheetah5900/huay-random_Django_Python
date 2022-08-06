from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from huayrandom.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('huayrandom.urls')),
    path('login/',Login,name='login'),
    path('logout/',views.LogoutView.as_view(template_name='logout.html'),name='logout')
]
