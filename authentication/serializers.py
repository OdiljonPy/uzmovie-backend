from rest_framework.serializers import ModelSerializer
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile_picture', 'is_verified', 'is_active')

