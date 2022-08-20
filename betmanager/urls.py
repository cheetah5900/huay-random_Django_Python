from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from huayrandom.views import *
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings  # ดึงไฟล์ settings มาใส่ในไฟล์นี้ ให้ใช้ MEDIA ได้

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('huayrandom.urls')),
    path('login/',Login,name='login'),
    path('logout/',views.LogoutView.as_view(template_name='logout.html'),name='logout')
]

# ทำให้ ระบบรู้ว่า URL ของไฟล์ MEDIA (MEDIA_URL) มี ไฟล์อยู่ที่ MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
