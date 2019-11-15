from django.contrib.auth.models import User
from pytz import unicode
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from .serializers import SubjectSerializer, TeacherProfileSerializer, StudentProfileSerializer, RegistrationSerializer, \
    UserSerializer
from classroom.models import Subject, Teacher, Student

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import permissions


class SubjectView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class TeacherProfileViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherProfileSerializer
    queryset = Teacher.objects.all()


class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    queryset = Student.objects.all()


@api_view(['POST', ])
def teacher_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully"
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token

            serializer_profile = TeacherProfileSerializer(
                data={"user": user.id, "gender": request.data["certification_number"]})
            if serializer_profile.is_valid():
                user_profile = serializer_profile.save()
            else:
                data = serializer_profile.errors
        else:
            data = serializer.errors

        return Response(data)


@api_view(['POST', ])
def student_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully"
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token

            serializer_profile = StudentProfileSerializer(data={"user": user.id, "gender": request.data["gender"]})
            if serializer_profile.is_valid():
                user_profile = serializer_profile.save()
            else:
                data = serializer_profile.errors
        else:
            data = serializer.errors

        return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user_detail_view(request, format=None):
    user_id = User.objects.filter(username=request.user)[0].id

    is_teacher = 0
    is_student = 0
    if Teacher.objects.filter(user_id=user_id) :
        is_teacher = 1

    if Student.objects.filter(user_id=user_id) :
        is_student = 1



    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
        'is_teacher' : is_teacher,
        'is_student' : is_student
    }
    return Response(content)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

