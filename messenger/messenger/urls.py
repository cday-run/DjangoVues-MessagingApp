
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #authentication routes
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),

    #api routes
    path('api/', include('core.urls'))
]
