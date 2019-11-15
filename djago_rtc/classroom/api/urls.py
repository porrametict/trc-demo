from .views import SubjectView, TeacherProfileViewSet, StudentProfileViewSet, student_registration_view, \
    teacher_registration_view, get_current_user_detail_view,Logout
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'classroom'

urlpatterns = [
    path('teacher_register', teacher_registration_view, name='register'),
    path('student_register', student_registration_view, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('current_user', get_current_user_detail_view, name="get_current_user"),
]
