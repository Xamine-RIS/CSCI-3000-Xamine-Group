from django.urls import path, include

from xamine import views, apiviews

urlpatterns = [
    path('order/<int:order_id>/', views.order, name='order'),
    path('order/<int:order_id>/upload', views.upload_file, name='submit_image'),
    path('order/<int:order_id>/send', apiviews.patient_email, name='patient_view'),
    path('order/<int:order_id>/schedule', views.schedule_order, name='schedule_time'),
    path('order/<int:order_id>/save', views.save_order, name='save_order'),

    path('', views.index, name='index'),

    path('patient/<int:pat_id>/', views.patient, name='patient'),
    path('patient/', views.patient_lookup, name='patient_lookup'),
    path('patient/new', views.new_patient, name='new_patient'),
    path('patient/<int:pat_id>/new-order', views.new_order, name='new_order'),

    
]