from rest_framework import viewsets, status
from rest_framework.response import Response
from core.senders.medicine import *
from core.senders.accounts import *
from core.retrievers.accounts import *
from core.retrievers.medicines import *
from core.utils import get_user_from_jwttoken
from rest_framework.permissions import IsAuthenticated


class MedicineViewset(viewsets.ViewSet):
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
            "data": get_all_service_providers(),
        }
        return Response(context, status=status.HTTP_200_OK)

    def list_service(self, request):
        """View for getting all service objects

        Args:
            request (http): get request
        """
        context = {"detail": "All Medicines", "medicines": get_all_medicine()}
        return Response(context, status=status.HTTP_200_OK)

    def list_ordered_medicine_of_customer(self, request):
        """View for getting all booked service by a customer

        Args:
            request (http): get request
        """
        user = get_user_from_jwttoken(request)
        # if user.user_type != "customer":
        #     context = {
        #         "detail": "You are not a customer"
        #     }
        #     return Response(context, status=status.HTTP_403_FORBIDDEN)
        # send_data = [{
        #     "id": data["order_id"],
        #     "date": data["date"],
        #     "time": data["time"],
        #     "status": data["status"],
        #     "organization_name": data["service"]["user"]["organization_name"],
        #     "price":data["service"]["price"],
        #     "title": data["service"]["title"],
        #     "category": data["service"]["category"]
        # } for data in send_booked_medicine_by_customer(user)]

        data = send_booked_medicine_by_customer(user)
        context = {"detail": "All ordered medicine", "services": data}
        return Response(context, status=status.HTTP_200_OK)

    def list_ordered_service_of_doctor(self, request):
        """View for getting all booked service by a provider

        Args:
            request (http): get request
        """
        user = get_user_from_jwttoken(request)
        # # if user.user_type != "service_provider":
        #     context = {
        #         "detail": "You are not a service provider"
        #     }
        #     return Response(context, status=status.HTTP_403_FORBIDDEN)
        # send_data = [{
        #     "id": data["scheduleservice_id"],
        #     "date": data["date"],
        #     "time": data["time"],
        #     "status": data["status"],
        #     "customer": data["customer"]["email"],
        #     "price":data["service"]["price"],
        #     "title": data["service"]["title"],
        #     "category": data["service"]["category"]
        # } for data in get_booked_service_by_provider(user)]
        data = send_ordered_medicine_by_docter(user)
        context = {"detail": "All ordered medicines for a doctor", "data": data}
        return Response(context, status=status.HTTP_200_OK)

    def list_all_service_by_category(self, request):
        """View for getting all service by category

        Args:
            request (http): get request
            category (str): category of the service
        """
        context = {
            "detail": "All Services",
            "serices": send_service_by_category(category),
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
            context = {"detail": "User not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if user.user_type != "service_provider":
            context = {"detail": "You are not a service provider"}
            return Response(context, status=status.HTTP_403_FORBIDDEN)

        services = get_serivce_by_user(user)
        if not services:
            context = {"detail": "Service provider not found"}
            return Response(context, status=status.HTTP_200_OK)
        context = {"detail": "Service provider services", "services": services}
        return Response(context, status=status.HTTP_200_OK)

    def list_service_provider_services(self, request):
        """Get the services of a service provider

        Args:
            request (http): get request
            id (uuid): service provider id
        """
        user = get_user_from_jwttoken(request)
        if not user:
            context = {"detail": "User not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        if user.user_type != "service_provider":
            context = {"detail": "You are not a service provider"}
            return Response(context, status=status.HTTP_403_FORBIDDEN)

        services = get_serivce_by_user(user)
        if not services:
            context = {"detail": "Service provider not found"}
            return Response(context, status=status.HTTP_200_OK)
        context = {"detail": "Service provider services", "services": services}
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        """Create Service

        Args:
            request (http): post request
        """
        title = request.data.get("title")
        description = request.data.get("description")
        category = request.data.get("category")
        price = request.data.get("price")
        thumnail = request.data.get("thumnail")
        user = get_user_from_jwttoken(request)
        medicine = create_medicine(request.data, request.FILES)
        context = {"detail": "Medicine created successfully", "medicine": medicine}
        return Response(context, status=status.HTTP_201_CREATED)

    def update_medicine(self, request, id):
        """Update Service

        Args:
            request (http): put request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)
        # if user.user_type != "service_provider":
        #     context = {
        #         "detail": "You are not a service provider"
        #     }
        #     return Response(context, status=status.HTTP_403_FORBIDDEN)
        medicine = get_medicine_by_id(id)
        if not medicine:
            context = {"detail": "medicine not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        medicine = update_medicine(medicine, request.data)
        context = {"detail": "medicine updated successfully", "medicine": medicine}
        return Response(context, status=status.HTTP_200_OK)

    def retrieve_medicine(self, request, id):
        """Retrieve Service

        Args:
            request (http): get request
            id (uuid): service id
        """
        medicine = get_medicine_by_id(id)
        if not medicine:
            context = {"detail": "Medicine not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        context = {
            "detail": "Medicine retrieved successfully",
            "medicine": MedicineSerializer(medicine).data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def delete_medicine(self, request, id):
        """Delete Service

        Args:
            request (http): delete request
            id (uuid): service id
        """
        user = get_user_from_jwttoken(request)
        # if user.user_type != "service_provider":
        #     context = {
        #         "detail": "You are not a service provider"
        #     }
        #     return Response(context, status=status.HTTP_403_FORBIDDEN)
        medicine = get_medicine_by_id(id)
        if not medicine:
            context = {"detail": "Medicine not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        medicine.delete()
        context = {"detail": "Medicine deleted successfully"}
        return Response(context, status=status.HTTP_200_OK)

    def list_orders(self, request):
        """List all orders

        Args:
            request (http): get request
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        context = {"detail": "All Orders", "orders": serializer.data}
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

    def get_permission(self):
        """Get permission for the viewset

        Returns:
            list: list of permissions
        """
        if self.action in [
            "create_service",
            "update_service",
            "delete_service",
            "book_service",
        ]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def retrieve_order(self, request, id):
        """Retrieve Order

        Args:
            request (http): get request
            id (uuid): order id
        """
        order = get_order_by_id(id)
        if not order:
            context = {"detail": "Order not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        context = {"detail": "Order retrieved successfully", "order": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def delete_order(self, request, id):
        """Delete Order

        Args:
            request (http): delete request
            id (uuid): order id
        """
        order = get_order_by_id(id)
        if not order:
            context = {"detail": "Order not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        context = {
            "detail": "Order deleted successfully",
        }
        return Response(context, status=status.HTTP_200_OK)

    def update_order_medicine(self, request, id):
        """Update Ordered

        Args:
            request (http): put request
        """
        order_status = request.data.get("status")
        order = get_order_by_id(id)
        if not order:
            context = {"detail": "Order not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        order = update_ordered_medicine_status(order, status=order_status)
        context = {
            "detail": "Order updated successfully",
        }
        return Response(context, status=status.HTTP_200_OK)


class CategoryViewset(viewsets.ViewSet):
    """View set for handling category related requests

    Args:
        viewsets (viewset): viewset class
    """

    def create(self, request):
        """Create Category

        Args:
            request (http): post request
        """
        category = create_category(request.data)
        if category:
            context = {
                "detail": "Category created successfully",
            }
            return Response(context, status=status.HTTP_201_CREATED)
        context = {
            "detail": "Category not created",
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """List all categories

        Args:
            request (http): get request
        """
        serializer = CategorySerializer(get_all_categories(), many=True)
        context = {"detail": "All Categories", "categories": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, id):
        """Retrieve Category

        Args:
            request (http): get request
            id (uuid): category id
        """
        category = get_category_by_id(id)
        if not category:
            context = {"detail": "Category not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        context = {
            "detail": "Category retrieved successfully",
            "category": serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def update(self, request, id):
        """Update Category

        Args:
            request (http): put request
            id (uuid): category id
        """
        name = request.data.get("name")
        category = get_category_by_id(id)
        if not category:
            context = {"detail": "Category not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        category = update_category(category, request.data)
        context = {
            "detail": "Category updated successfully",
        }
        return Response(context, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """Delete Category

        Args:
            request (http): delete request
            id (uuid): category id
        """
        category = get_category_by_id(id)
        if not category:
            context = {"detail": "Category not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        context = {
            "detail": "Category deleted successfully",
        }
        return Response(context, status=status.HTTP_200_OK)
