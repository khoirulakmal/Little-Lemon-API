from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from LittleLemonAPI import views

urlpatterns = [
    path("menu-items/", views.MenuItemList.as_view()),
    path("menu-items/<int:pk>/", views.MenuItemDetail.as_view()),
    path("", include('djoser.urls')),
    path("groups/<slug:group>/users/", views.UserList.as_view()),
    path("groups/<slug:group>/users/<int:pk>/", views.UserDelete.as_view()),
    path("cart/menu-items/", views.CartItemList.as_view()),
    path("orders/", views.OrderList.as_view()),
    path("orders/<int:pk>/", views.OrderDetail.as_view()),
    # path("groups/manager/users/", views.managers)
]
