from django.http import HttpResponse 
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.
def index(request):
     return render(request, "authentication/login.html")

def dashboard(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()
    context = {
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_notifications_count
    }
    return render(request, "students/student-dashboard.html", context)


@login_required
def mark_notifications_as_read(request):
    if request.method == "POST":
         notification = Notification.objects.filter(user=request.user, is_read=False)
         notification.update(is_read=True)
         return JsonResponse({'status' :'Success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
     if request.method == "POST":
           notification = Notification.objects.filter(user=request.user)
           notification.delete()
           return JsonResponse({'status' :'Success'})
     return HttpResponseForbidden


def view_all_notifications(request):
    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
    context = {
        'all_notifications': all_notifications,
        'unread_notification_count': unread_notification_count
    }
    return render(request, 'notifications.html', context)


# Teacher Views


          