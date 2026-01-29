from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('student/', include('student.urls')),
    path('student-details.html', TemplateView.as_view(template_name='students/student-details.html'), name='student_details_page'),
    path('edit-student.html', TemplateView.as_view(template_name='students/edit-student.html'), name='edit_student_page'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('notification/mark-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notification/clear-all/', views.clear_all_notification, name='clear_all_notification'),
    path('notifications/', views.view_all_notifications, name='view_all_notifications'),
]