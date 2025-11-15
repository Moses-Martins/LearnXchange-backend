from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_image_url = serializers.URLField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['bio'] = self.validated_data.get('bio', '')
        data['profile_image_url'] = self.validated_data.get('profile_image_url', '')

        return data
    
    def save(self, request):
        user = super().save(request)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.bio = self.cleaned_data.get('bio')
        user.profile_image_url = self.cleaned_data.get('profile_image_url')

        user.save()
        return user