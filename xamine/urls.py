from django.urls import path, include

from xamine import views

urlpatterns = [
    path('', views.index, name='index'),

]