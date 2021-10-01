from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.user_signup, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('studenthome/', views.student_home, name='student_home'),
    path('studentprofile/', views.student_profile, name='student_profile'),
    path('studentupdate/', views.student_update, name='student_update'),
    path('studentleave/', views.student_leave_apply, name='student_leave_apply'),
    path('studentfeedback/', views.student_feedback, name='student_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
