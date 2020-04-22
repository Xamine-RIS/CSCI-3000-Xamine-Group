from django.urls import path, include

from xamine import views, apiviews

urlpatterns = [
    path('order/<int:order_id>/', views.order, name='order'),
    path('order/<int:order_id>/upload', views.upload_file, name='submit_image'),
    path('order/<int:order_id>/send', apiviews.patient_email, name='patient_view'),
    path('order/<int:order_id>/schedule', views.schedule_order, name='schedule_time'),

    path('', views.index, name='index'),

    path('patient/<int:pat_id>/', views.patient, name='patient'),

    
]