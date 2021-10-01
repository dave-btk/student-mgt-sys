from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('staffhome/', views.staff_home, name='staff_home'),
    path('staffprofile/', views.staff_profile, name='staff_profile'),
    path('staffupdate/', views.staff_update, name='staff_update'),
    path('stafffeedback/', views.staff_feedback, name='staff_feedback'),
    path('staffleave/', views.staff_leave_apply, name='staff_leave_apply'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
