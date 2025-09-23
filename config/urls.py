from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('collections/', include('collections_app.urls')),
    path('search/', include('search.urls')),

    path('home/', views.home, name='home_page'),   # /home/
    path('', views.home, name='index'),            # главная страница /
]
