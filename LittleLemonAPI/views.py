from django.shortcuts import *
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import MenuItem
from .serializers import *
from .permissions import *
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend




# TODO MenuItemList and MenuitemDetail Permission can be refactor (Find a way to do it)
class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['__all__'],
         'POST': ['Manager'],
         'PUT': ['Manager'],
         'DELETE': ['Manager'],
     }
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'price']
    
class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager|IsAdminUser]
    User_Group = {
        'manager':'Manager',
        'delivery-crew':'Delivery Crew',
    }
    
    # Get user list based on url slug
    def list(self, request, **kwargs):
        # get the user request group
        slug = kwargs['group']
        user_group = Group.objects.get(name=self.User_Group[slug])
        
        # filter the queryset to only include users in the user request group
        queryset = self.get_queryset().filter(groups=user_group)
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # Assign user to group based on url slug
    def create(self, request, **kwargs):
        username = request.data.get('username', None)
        if not username:
            return Response({'detail': 'Username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # check if user with given username exists
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({'detail': f'User with username {username} does not exist. Please register user first before making a request.'}, status=status.HTTP_400_BAD_REQUEST)

        # update the user's group
        slug = kwargs['group']
        group = Group.objects.get(name=self.User_Group[slug])
        user.groups.clear()
        user.groups.add(group)

        # serialize the user object and return the response
        serializer = self.get_serializer(user)
        return Response({'message': f'User added to {self.User_Group[slug]} group'}, status=status.HTTP_200_OK)
  
class UserDelete(APIView):
    permission_classes = [IsManager|IsAdminUser]
    User_Group = {
        'manager':'Manager',
        'delivery-crew':'Delivery Crew',
    }
    
    def delete(self, group, pk):
        user = get_object_or_404(User, id=pk)
        group = Group.objects.get(name=self.User_Group[group])
        if user.groups.filter(id=group.id).exists():
            user.groups.remove(group) # remove user from group
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class CartItemList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs): 
        # Set the authenticated user as the user id for these cart items
        data = request.data.copy()
        data['user'] = request.user.id
        
        # Check if the menu item exists in the database
        menuitem_id = data.get('menuitem')
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the price based on quantity and unit price
        quantity = int(data.get('quantity', 0))
        unit_price = menuitem.price
        data['unit_price'] = unit_price
        data['price'] = quantity * unit_price

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        # Get all the cart items in the queryset
        queryset = self.filter_queryset(self.get_queryset())
        # Check permissions
        self.check_permissions(request)
        # Delete all the cart items in the queryset
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['delivery', 'status', 'title']
    
    def get_queryset(self):
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name='Manager').exists():
            # Returns all orders with order items by all users
            return Order.objects.all()
        elif user_groups.filter(name='Delivery Crew').exists():
            # Returns all orders with order items assigned to the delivery crew
            return Order.objects.filter(delivery=self.request.user)
        else:
            # Returns all orders with order items created by this user
            return Order.objects.filter(user=self.request.user).prefetch_related('user')
    
    def create(self, request):
        user = self.request.user
       # Get current cart items from the cart endpoints
        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            return Response({'error': 'No item in cart.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Order object for the current user
        order = Order.objects.create(user=user, total=0, date=datetime.now())

        # Loop through the cart items and create OrderItem objects
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.menuitem.price,
                price=cart_item.quantity * cart_item.menuitem.price,
            )

            # Update the total price of the order
            order.total += order_item.price

        # Save the updated order
        order.save()

        # Delete all items from the cart for this user
        cart_items.delete()
        return Response({'status': 'Order created.'}, status=status.HTTP_200_OK)

    
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['__all__'],
         'PUT': ['Manager'],
         'PATCH': ['Manager'],
         'PATCH': ['Delivery Crew'],
         'DELETE': ['Manager'],
     }
    
    def get(self, request, pk):
        # Check if order belongs to current user
        order = Order.objects.filter(id=pk, user=request.user).first()
        if not order:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Return order items
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk):
# payload = status, delivery crew
# get status and delivery crew id -> check delivery crew (if it match with user models proccess)
# assign delivery crew to serializers and change status if status exist in payload
        if not request.user.groups.filter(name='Delivery Crew').exists():
            delivery_crew_id = request.data.get('delivery')
            if not delivery_crew_id:
                return Response({'error': 'No delivery crew assigned.'}, status=status.HTTP_400_BAD_REQUEST)
            
            #if user(deliverycrewid) not in delivery group return error
            delivery_crew_user = get_object_or_404(User, id=delivery_crew_id)
            user_groups = delivery_crew_user.groups.all()
            if not user_groups.filter(name='Delivery Crew').exists():
                return Response({'error': 'Delivery Crew not assigned in database'}, status=status.HTTP_400_BAD_REQUEST)
        
        status_order = request.data.get('status')
        if not status_order:
            return Response({'error': 'Status order not assigned.'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = self.get_object()
        if request.user.groups.filter(name='Delivery Crew').exists():
            serializer = self.get_serializer(instance, data={"status": request.data.get("status")}, partial=True)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)  
        