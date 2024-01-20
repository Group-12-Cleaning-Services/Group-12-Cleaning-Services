from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.senders.profile import *
from core.retrievers.accounts import *
from core.utils import *
import threading

class ProfileViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """Profile viewset"""

    def create(self, request):
        """Create user profile"""
        user = get_user_from_jwttoken(request)
        if not user:
            context = {
                'detail': 'User does not exist'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = create_profile(request.data)
        print(f"profile {profile}")
        user.profile = get_profile_by_id(profile["profile_id"])
        user.save()
        if user.user_type == "service_provider":
            receipeint = create_transfer_receipient(user.profile)
            if receipeint:
                Transaction.objects.create(user=user, transfer_receipient_code=receipeint["data"]["recipient_code"])
        context = {
            "detail": "Profile created successfully", "profile": profile,
            }
        return Response(context, status=status.HTTP_201_CREATED)


    def update(self, request):
        """Update user profile"""
        user = get_user_from_jwttoken(request)
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
        profile = update_profile(request.data, profile)
        context = {
            "detail": "Profile updated successfully", "profile": profile
            }
        return Response(context, status=status.HTTP_200_OK)




    def retrieve(self, request):
        """Retrieve user profile"""
        user = get_user_from_jwttoken(request)
        if not user:
            context = {
                "detail": "user does not exist"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        profile = get_profile_by_user_id(user_id=user.user_id)
        if not profile:
            context = {
                "detail": "profile does not exists", 
                "profile": None
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "profile": send_profile_information(profile)
        }
        return Response(context, status=status.HTTP_200_OK)


    def delete(self, request):
        """Delete user profile"""
        pass