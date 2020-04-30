from django.urls import path, include

from xamine import views, apiviews

urlpatterns = [
    path('', views.index, name='index'),  # view dashboard

    path('order/', views.public_order, name='public_order'),  # Patient viewing of orders
    path('order/<int:order_id>/', views.order, name='order'),  # Internal viewing and submitting of orders
    path('order/<int:order_id>/upload', views.upload_file, name='submit_image'),  # Uploading images for order
    path('order/<int:order_id>/send', apiviews.patient_email, name='patient_view'),  # Send patient view email
    path('order/<int:order_id>/schedule', views.schedule_order, name='schedule_time'),  # Schedule our order
    path('order/<int:order_id>/save', views.save_order, name='save_order'),  # Save radiology report without finalizing.

    path('patient/<int:pat_id>/', views.patient, name='patient'),  # View patient info
    path('patient/', views.patient_lookup, name='patient_lookup'),  # lookup patients by DOB
    path('patient/new', views.new_patient, name='new_patient'),  # Submit new patient info
    path('patient/<int:pat_id>/new-order', views.new_order, name='new_order'),  # Start new order for patient

    path('image/<int:img_id>/remove', views.remove_file, name='remove_image'),  # Remove specified image

]