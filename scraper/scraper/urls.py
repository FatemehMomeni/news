from django.contrib import admin
from django.urls import path
from news import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('blog.html', views.blog, name="blog"),
    path('blog2.html', views.blog2, name="blog2"),
]
