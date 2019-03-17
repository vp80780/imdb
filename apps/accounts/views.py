from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CreateEmailUserSerializer, AuthTokenSerializer, UpdateUserInfoSerializer
from .models import EmailUser
# Create your views here.


# Any user can login with email and password and get Token in response
class ObtainAuthToken(OriginalObtain):
    def post(self, request, require_validated=True):
        serializer_class = AuthTokenSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data['user']
        except Exception as e:
            return Response(data={'errorMessage': serializer.validated_data}, status=200)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'result': 'success',
            'email': user.email,
            'token': token.key,
            'id': user.id,
            })

obtain_auth_token = ObtainAuthToken.as_view()


# This will help in creating accounts using email and password as well as user can update their profile by provide user ID.
class CreateEmailUserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateEmailUserSerializer
    permission_classes = (AllowAny,)
    queryset = EmailUser.objects.all()

    def get_queryset(self):
        q = self.queryset
        return q.filter(first_name='ksjdfksfskjdhfjshf')

    def create(self, validated_data):
        if 'id' in self.request.data:
            user = self.queryset.filter(id=self.request.data['id']).first()
            serializer = UpdateUserInfoSerializer(
                instance=user,
                data=self.request.data
            )
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            return Response(data={'id':user.id})

        user = self.create_user_api(validated_data)
        if user == False:
            user = EmailUser.objects.filter(email=self.request.data['email'])
            if user:
                return Response(data={'data':{'result':'Email id is already exist.'}})

        return Response(data={'data':{'id': user.id, 'email': user.email, 'result':'success'}})

    def create_user_api(self, validated_data):
        serializer = CreateEmailUserSerializer(data=self.request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return False
        user=serializer.save()
        user.set_password(self.request.data['password'])
        user.save()
        return user
