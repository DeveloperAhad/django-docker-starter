from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth.models import User
from utlity.token_generator import reset_password_token_generator


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class AdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if not user.check_password(attrs['password']):
                raise Exception('Wrong password!')
        except Exception:
            raise serializers.ValidationError({"password": "Email or password is incorrect"})
        return attrs


class ResetPasswordSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password do not match."})

        if attrs['uuid'] is not None and attrs['token'] is not None:
            user_id = force_text(urlsafe_base64_decode(attrs['uuid']))
            user = User.objects.get(pk=user_id)
            if not reset_password_token_generator.check_token(user, attrs['token']):
                raise serializers.ValidationError({"non_field_errors": ["Given token or uuid has expired"]})
        return attrs


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirmation = serializers.CharField()

    def validate_old_password(self, value):
        current_user = self.context['request'].user

        if not current_user.check_password(value):
            raise serializers.ValidationError('Old password do not match')

        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password', None)
        new_password_confirmation = attrs.get('new_password_confirmation', None)

        if not new_password == new_password_confirmation:
            raise serializers.ValidationError({
                'new_password_confirmation': ['The New password confirmation field confirmation does not match']
            })

        return attrs
