from django.urls import path

from . import views

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("cart/add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<int:order_id>/confirmation/", views.order_confirmation, name="order_confirmation"),
    path("orders/", views.order_history, name="order_history"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("owner/restaurants/new/", views.restaurant_create, name="restaurant_create"),
    path("owner/restaurants/<int:pk>/edit/", views.restaurant_edit, name="restaurant_edit"),
    path("owner/restaurants/<int:restaurant_pk>/menu/", views.menu_item_list, name="menu_item_list"),
    path("owner/restaurants/<int:restaurant_pk>/menu/new/", views.menu_item_create, name="menu_item_create"),
    path("owner/restaurants/<int:restaurant_pk>/menu/<int:item_pk>/edit/", views.menu_item_edit, name="menu_item_edit"),
    path("owner/restaurants/<int:restaurant_pk>/menu/<int:item_pk>/delete/", views.menu_item_delete, name="menu_item_delete"),
    path("owner/restaurants/<int:restaurant_pk>/orders/", views.owner_orders, name="owner_orders"),
    path("owner/orders/<int:order_pk>/status/", views.update_order_status, name="update_order_status"),
    path("cart/decrease/<int:item_id>/", views.decrease_cart_item, name="decrease_cart_item"),
]