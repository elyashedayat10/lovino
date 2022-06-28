from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True, required=False)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'user',
            'user_name',
            'province',
            'city',
            'first_name',
            'last_name',
            'bio',
            'gender',
            'birthdate',
            'age',
        )

    def get_age(self, obj):
        return obj.get_age

    def get_liked(self,obj):
        user =  self.context['request'].user
        if obj.user in user.likes_likes_to:



class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
