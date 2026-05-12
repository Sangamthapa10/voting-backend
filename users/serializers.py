from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    profile_image = serializers.SerializerMethodField()  # Updated

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'full_name', 'email', 'phone',
            'password', 'email_verified', 'verification_code', 'profile_image'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'verification_code': {'write_only': True},
            'email_verified': {'read_only': True},
        }

    def get_profile_image(self, obj):
        """Return full URL for profile image"""
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def create(self, validated_data):
        if 'full_name' in validated_data and not validated_data.get('username'):
            validated_data['username'] = validated_data['full_name']
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user