from django.contrib import admin
from django.urls import path, include
from src.api.api import api
# from config_socketio.settings import socket_io_server
from django.conf.urls.static import static

from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('src.users_app.urls')), 
    # path('socket_io/', socket_io_server),
    path('api/', api.urls),

    
]
