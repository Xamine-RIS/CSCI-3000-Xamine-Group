from django.urls import path

from . import views

app_name = 'results_portal'
urlpatterns = [
    path('', views.index, name='index')
]