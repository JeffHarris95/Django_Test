# from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('Survey_App.urls')),
    # path('admin/', admin.site.urls),
]
