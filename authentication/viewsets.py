from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import LoginSerializer, ResetPasswordSendSerializer, ResetPasswordSerializer, \
    AccountSerializer, ChangePasswordSerializer

from utlity.serializers import EmptySerializer
from utlity.token_generator import reset_password_token_generator
from utlity.viewsets import InitialModelViewSet
from .tasks import send_account_reset_password_email


class AuthViewSets(InitialModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'login_view':
            return LoginSerializer
        elif self.action == 'reset_password_send':
            return ResetPasswordSendSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return EmptySerializer

    def get_permissions(self):
        if self.action in ['login_view', 'reset_password_send', 'reset_password']:
            self.permission_classes = [AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def list(self, request):

        return Response([
            'Auth API endpoints',
            {

                "Login": f"{request.build_absolute_uri()}login/",
                "Reset password send": f"{request.build_absolute_uri()}reset-password/send/",
                "Reset password": f"{request.build_absolute_uri()}reset-password/",
                "Change password": f"{request.build_absolute_uri()}change-password/",
                "Account": f"{request.build_absolute_uri()}account/",
            }
        ])

    @action(detail=False, methods=['POST'], name='Login Verify', url_path='login')
    def login_view(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], name='Reset Passwort Send', url_path='reset-password/send')
    def reset_password_send(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.data['email'])
                uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = reset_password_token_generator.make_token(user)
                context = {
                    'url': f'{settings.FRONT_END_URL}/auth/reset-password?uuid={uidb64}&token={token}'
                }
                send_account_reset_password_email.delay(serializer.data['email'], context)
                return Response({'message': 'Reset password email send'})
            except User.DoesNotExist:
                return Response({'message': 'Reset password email send'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], name='Reset Passwort', url_path='reset-password')
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id = force_text(urlsafe_base64_decode(serializer.data['uuid']))
            user = User.objects.get(pk=id)
            user.password = make_password(serializer.data['password2'])
            user.save()
            return Response({'message': 'Your password has been reset successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], name='Change Password', detail=False, url_path='change-password')
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        current_user = request.user
        current_user.set_password(serializer.validated_data['new_password'])
        current_user.save()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], name='Auth User Account', url_path='account')
    def account(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = AccountSerializer(user)
        return Response(serializer.data)
