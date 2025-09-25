from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recipes.views import HomePageView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),   # кастомные юзеры
    path('recipes/', include('recipes.urls')),
    path('collections/', include('collections_app.urls')),
    path('search/', include('search.urls')),
    path('', HomePageView.as_view(), name="home"),  # главная /
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)