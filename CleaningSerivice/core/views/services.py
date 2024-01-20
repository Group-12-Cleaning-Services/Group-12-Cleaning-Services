from rest_framework import viewsets, status
from rest_framework.response import Response
from core.senders.services import *
from core.senders.accounts import *
from core.retrievers.accounts import *
from core.retrievers.services import *
from core.utils import get_user_from_jwttoken
from rest_framework.permissions import IsAuthenticated

class ServiceViewset(viewsets.ViewSet):
    """View set for handling service related requests

    Args:
        viewsets (viewset): viewset class
    """
    def list_service_providers(self, request):
        """View for getting all service providers

        Args:
            request (http): get request
        """
        context = {
            "detail": "All Service Providers",
            "data": get_all_service_providers()
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def list_service(self, request):
        """View for getting all service objects

        Args:
            request (http): get request
        """
        context = {
            "detail": "All Services",
            "services": send_all_services()
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    def list_booked_service_of_customer(self, request):
        """View for getting all booked service by a customer

        Args:
            request (http): get request
        """
        user = get_user_from_jwttoken(request)
        if user.user_type != "customer":
            context = {
                "detail": "You are not a customer"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        send_data = [{
            "id": data["scheduleservice_id"],
            "date": data["date"],
            "time": data["time"],
            "status": data["status"],
            "organization_name": data["service"]["user"]["organization_name"],
            "price":data["service"]["price"],
            "title": data["service"]["title"],
            "category": data["service"]["category"]
        } for data in send_booked_service_by_customer(user)]

        context = {
            "detail": "All booked service by a customer",
            "services": send_data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def list_booked_service_of_provider(self, request):
        """View for getting all booked service by a provider

        Args:
            request (http): get request
        """
        user = get_user_from_jwttoken(request)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        send_data = [{
            "id": data["scheduleservice_id"],
            "date": data["date"],
            "time": data["time"],
            "status": data["status"],
            "customer": data["customer"]["email"],
            "price":data["service"]["price"],
            "title": data["service"]["title"],
            "category": data["service"]["category"]
        } for data in get_booked_service_by_provider(user)]

        context = {
            "detail": "All booked service by a provider",
            "services": send_data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    def list_all_service_by_category(self, request):
        """View for getting all service by category

        Args:
            request (http): get request
            category (str): category of the service
        """
        context = {
            "detail": "All Services",
            "serices": send_service_by_category(category)
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def get_service_provider_services(self, request, id):
        """Get the services of a service provider

        Args:
            request (http): get request
            id (uuid): service provider id
        """
        user = get_user_by_id(id)
        if not user:
            context = {
                "detail": "User not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        
        services = get_serivce_by_user(user)
        if not services:
            context = {
                "detail": "Service provider not found"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "detail": "Service provider services",
            "services": services
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    def list_service_provider_services(self, request):
        """Get the services of a service provider

        Args:
            request (http): get request
            id (uuid): service provider id
        """
        user = get_user_from_jwttoken(request)
        if not user:
            context = {
                "detail": "User not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        
        services = get_serivce_by_user(user)
        if not services:
            context = {
                "detail": "Service provider not found"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "detail": "Service provider services",
            "services": services
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def create_service(self, request):
        """Create Service

        Args:
            request (http): post request
        """
        title  = request.data.get("title")
        description = request.data.get("description")
        category = request.data.get("category")
        price = request.data.get("price")
        thumnail = request.data.get("thumnail")
        user = get_user_from_jwttoken(request)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        service = create_service(user, request.data)
        context = {
            "detail": "Service created successfully",
            "service": service
        }
        return Response(context, status=status.HTTP_201_CREATED)
    
    
    def update_service(self, request, id):
        """Update Service

        Args:
            request (http): put request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        service = get_service_by_id(id)
        if not service:
            context = {
                "detail": "Service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        service = update_service(service, request.data)
        context = {
            "detail": "Service updated successfully",
            "service": service
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    def retrieve_service(self, request, id):
        """Retrieve Service

        Args:
            request (http): get request
            id (uuid): service id
        """
        service = get_service_by_id(id)
        if not service:
            context = {
                "detail": "Service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        context = {
            "detail": "Service retrieved successfully",
            "service": service
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    def delete_service(self, request, id):
        """Delete Service

        Args:
            request (http): delete request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a service provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        service = get_service_by_id(id)
        if not service:
            context = {
                "detail": "Service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        service.delete()
        context = {
            "detail": "Service deleted successfully"
        }
        return Response(context, status=status.HTTP_200_OK)
        
        
    # def book_service(self, request, id):
    #     """Book Service

    #     Args:
    #         request (http): post request
    #         id (uuid): service id
    #     """
    #     user = get_user_from_jwttoken(request)
    #     if user.user_type != "customer":
    #         context = {
    #             "detail": "You are not a customer"
    #         }
    #         return Response(context, status=status.HTTP_403_FORBIDDEN)
    #     service = get_service_by_id(id)
    #     if not service:
    #         context = {
    #             "detail": "Service not found"
    #         }
    #         return Response(context, status=status.HTTP_404_NOT_FOUND)
    #     schedule_service = book_service(service, user, request.data)
    #     context = {
    #         "detail": "Service booked successfully",
    #         "schedule_service": schedule_service
    #     }
    #     return Response(context, status=status.HTTP_200_OK)
    
    
    def cancel_booked_service(self, request, id):
        """Cancel Booked Service

        Args:
            request (http): delete request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)
        # if user:
        #     context = {
        #         "detail": "You are not a customer"
        #     }
        #     return Response(context, status=status.HTTP_403_FORBIDDEN)
        schedule_service = get_booked_service_by_id(id)
        if not schedule_service:
            context = {
                "detail": "Schedule service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        schedule_service.delete()
        context = {
            "detail": "Schedule service deleted successfully"
        }
        return Response(context, status=status.HTTP_200_OK)
        
    
    
    def service_feedback(self, request, id):
        """ Service Feedback

        Args:
            request (http): post request
            id (uuid): service id
        """
        review = request.data.get("review")
        rating = request.data.get("rating")
        user = get_user_from_jwttoken(request)
        if user.user_type != "customer":
            context = {
                "detail": "You are not a customer"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        service = get_booked_service_by_id(id)
        if not service or service.customer != user:
            context = {
                "detail": "Service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        feedback = create_feedback(review, service, rating)
        context = {
            "detail": "Feedback created successfully",
            "feedback": feedback
        }
        return Response(context, status=status.HTTP_201_CREATED)
    
    
    def get_permission(self):
        """Get permission for the viewset

        Returns:
            list: list of permissions
        """
        if self.action in ["create_service", "update_service", "delete_service", "book_service"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    

    def update_booked_service(self, request, id):
        """Update Booked Service

        Args:
            request (http): put request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)  
        service_status = request.data.get("status")
        if user.user_type != "service_provider":
            context = {
                "detail": "You are not a provider"
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        schedule_service = get_booked_service_by_id(id)
        if not schedule_service:
            context = {
                "detail": "Schedule service not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        schedule_service = update_booked_service_status(schedule_service, status=service_status)
        context = {
            "detail": "Schedule service updated successfully",
        }
        return Response(context, status=status.HTTP_200_OK)