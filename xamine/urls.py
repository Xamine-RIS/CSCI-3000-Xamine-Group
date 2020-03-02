from django.urls import path, include

from xamine import views

urlpatterns = [
    path('patient/<int:patid>', views.index, name='index'),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('', views.index, name='index'),

]