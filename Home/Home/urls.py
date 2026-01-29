from django.contrib import admin
from django.urls import path, include
from home_auth import views as auth_views  # added
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("school.urls")),
    path('student/', include(("student.urls", "student"), namespace="student")),
    path('authentication/', include('home_auth.urls')),
    path('forgot-password/', auth_views.forgot_password_view),  # new root-level mapping
    path('reset_password/<str:token>/', auth_views.reset_password_view),  # new root-level mapping
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)