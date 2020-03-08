from django.urls import path, include

from xamine import views

urlpatterns = [
    path('order/', views.order, name='order'),
    path('', views.index, name='index'),
]
