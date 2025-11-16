from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    path('superadmin/', admin.site.urls, name='admin'),
    path('catalog/', include('catalog.urls')),
]
