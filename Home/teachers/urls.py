from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('<str:slug>/', views.view_teacher, name='view_teacher'),
    path('<str:slug>/edit/', views.edit_teacher, name='edit_teacher'),
    path('<str:slug>/delete/', views.delete_teacher, name='delete_teacher'),
    
]
