from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.senders.profile import *
from core.retrievers.accounts import *
from rest_framework_simplejwt.tokens import AccessToken
from core.utils import *


class ProfileViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """Profile viewset"""
    
    def list(self, request):
        """List user profile"""
        profiles = all_profiles()
        context = {"detail": "Profiles retrieved successfully", "profiles": profiles}
        return Response(context, status=status.HTTP_200_OK)


    def create(self, request):
        """Create user profile"""

        user = get_user_from_jwttoken(request)
        if  user.profile:
            context = {
                'detail': 'profile already exist'
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        
        profile = create_profile(request.data)
        user.profile = get_profile_by_id(profile["profile_id"])
        user.save()
        context = {"detail": "Profile created successfully", "profile": profile}
        return Response(context, status=status.HTTP_201_CREATED)
        

    def update(self, request):
        """Update user profile"""
        user = get_user_from_jwttoken(request)
        if not user.profile:
            context = {
                'detail': 'Profile does not exist'
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        # profile = get_profile_by_user_id(user_id=user.user_id)
        # if not profile:
        #     context = {
        #         'detail': 'Profile does not exist'
        #     }
        #     return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = update_profile(request.data, user.profile)
        user.profile = get_profile_by_id(profile["profile_id"])
        user.save()
        context = {"detail": "Profile updated successfully", "profile": profile}
        return Response(context, status=status.HTTP_200_OK)
    
    


    def retrieve(self, request):
        """Retrieve user profile"""
        pass

    def delete(self, request):
        """Delete user profile"""
        pass