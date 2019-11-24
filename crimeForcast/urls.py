
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vis/', include('visual.urls')),
    path('predict/', include('predict.urls')),
    path('accounts/', include('users.urls')),
]


# added to serve static files
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
