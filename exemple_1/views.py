from api.serializers import TokenSerializer, LoginSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from nc_accounts.serializers import LoginSerializer, AccountCreateSerializer, \
    AccountDetailSerializer, \
    ChangePasswordSerializer
from rest_framework.response import Response


class CreateTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({'id': instance.id})


class AccountCreateView(APIView):
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({'id': instance.id})


class AccountDetailView(APIView):
    def get(self, request):
        serializer = AccountDetailSerializer(instance=request.user.account)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']

        )
        if user is None:
            return Response({'detail': 'fail'})

        login(request, user)
        return Response({'detail': 'ok'})


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated():
            return Response()
        logout(request)
        return Response({'detail': 'ok'})


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'detail': 'success'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
