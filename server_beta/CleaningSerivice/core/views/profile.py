from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.senders.profile import *
from core.retrievers.accounts import *

class ProfileViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """Profile viewset"""

    def create(self, request):
        """Create user profile"""
        user = request.user.email
        if not user:
            context = {
                'detail': 'User does not exist'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = create_profile(request.data)
        user.profile = profile
        user.save()
        context = {"detail": "Profile created successfully", "profile": profile}
        return Response(context, status=status.HTTP_201_CREATED)


    def update(self, request):
        """Update user profile"""
        user = request.user.email
        if not user:
            context = {
                'detail': 'User does not exist'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = get_profile_by_user_id(user_id=user.user_id)
        if not profile:
            context = {
                'detail': 'Profile does not exist'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = update_profile(request.data)
        context = {"detail": "Profile updated successfully", "profile": profile}
        return Response(context, status=status.HTTP_200_OK)




    def retrieve(self, request):
        """Retrieve user profile"""
        pass

    def delete(self, request):
        """Delete user profile"""
        pass