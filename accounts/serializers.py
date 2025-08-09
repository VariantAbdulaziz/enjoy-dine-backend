from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from allauth.account.utils import  user_pk_to_url_str
from rest_framework.exceptions import ValidationError
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from allauth.account import app_settings as allauth_account_settings
from allauth.utils import get_username_max_length


User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_account_settings.SIGNUP_FIELDS['username']['required'])
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email=serializers.EmailField(required=allauth_account_settings.SIGNUP_FIELDS['username']['required'])
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.SIGNUP_FIELDS['username']['required'],
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'country']

    def save(self, request=None):
        print(self.validated_data)
        user = get_user_model().objects.create_user(
            username=self.validated_data['username'],
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            country=self.validated_data['country']
        )
        return user

class VerifyEmailByCodeSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=128)
    email = serializers.EmailField()

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def validate(self, attrs):
        uid = attrs['uid']
        try:
            user = User.objects.get(pk=uid)
            attrs["uid"] = uid = user_pk_to_url_str(user)
            return super().validate(attrs)
        except ValidationError as e:

            raise

    def save(self):
        return super().save()

