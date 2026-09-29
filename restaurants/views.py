from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import MenuItem, Order, OrderItem, Restaurant


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_open=True)

    cuisine = request.GET.get("cuisine")
    if cuisine:
        restaurants = restaurants.filter(cuisine__icontains=cuisine)

    cuisines = (
        Restaurant.objects.filter(is_open=True)
        .values_list("cuisine", flat=True)
        .distinct()
    )

    return render(
        request,
        "restaurants/restaurant_list.html",
        {"restaurants": restaurants, "cuisines": cuisines, "selected_cuisine": cuisine},
    )


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_open=True)
    menu_items = restaurant.menu_items.filter(is_available=True)
    return render(
        request,
        "restaurants/restaurant_detail.html",
        {"restaurant": restaurant, "menu_items": menu_items},
    )


@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart = Cart(request)
    cart.add(menu_item)
    return redirect("restaurant_detail", pk=menu_item.restaurant_id)


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, "restaurants/cart_detail.html", {"cart": cart})


@login_required
def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect("cart_detail")


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("restaurant_list")

    if request.method == "POST":
        first_item = next(iter(cart))
        restaurant_id = first_item["menu_item"].restaurant_id

        order = Order.objects.create(
            customer=request.user,
            restaurant_id=restaurant_id,
            total=cart.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                menu_item=item["menu_item"],
                quantity=item["quantity"],
                price=item["menu_item"].price,
            )
        cart.clear()
        return redirect("order_confirmation", order_id=order.id)

    return render(request, "restaurants/checkout.html", {"cart": cart})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "restaurants/order_confirmation.html", {"order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "restaurants/order_history.html", {"orders": orders})