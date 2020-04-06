from django.urls import path, include

from xamine import views

urlpatterns = [
    path('order/', views.order, name='order_prototype'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('', views.index, name='index'),
    path('patient/', views.patient, name='patient_prototype'),
    path('patient/<int:pat_id>/', views.patient, name='patient'),
]