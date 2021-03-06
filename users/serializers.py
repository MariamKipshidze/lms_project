from users.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "status", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def save(self):
        user = User(
            email=self.validated_data["email"],
            status=self.validated_data["status"]
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": 'Password should match'})

        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "status", "password", "password2"]