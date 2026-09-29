from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import MenuItem, Order, OrderItem, Restaurant
from accounts.decorators import customer_required, owner_required
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


@customer_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart = Cart(request)
    cart.add(menu_item)
    return redirect("restaurant_detail", pk=menu_item.restaurant_id)


@customer_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, "restaurants/cart_detail.html", {"cart": cart})


@customer_required
def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect("cart_detail")


@customer_required
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


@customer_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "restaurants/order_confirmation.html", {"order": order})


@customer_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "restaurants/order_history.html", {"orders": orders})

@customer_required
def decrease_cart_item(request, item_id):
    cart = Cart(request)
    cart.decrease(item_id)
    return redirect("cart_detail")

from accounts.decorators import owner_required
from .forms import MenuItemForm, RestaurantForm


@owner_required
def owner_dashboard(request):
    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, "restaurants/owner_dashboard.html", {"restaurants": restaurants})


@owner_required
def restaurant_create(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect("owner_dashboard")
    else:
        form = RestaurantForm()
    return render(request, "restaurants/restaurant_form.html", {"form": form})


@owner_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect("owner_dashboard")
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, "restaurants/restaurant_form.html", {"form": form})


@owner_required
def menu_item_list(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    menu_items = restaurant.menu_items.all()
    return render(
        request,
        "restaurants/menu_item_list.html",
        {"restaurant": restaurant, "menu_items": menu_items},
    )


@owner_required
def menu_item_create(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            return redirect("menu_item_list", restaurant_pk=restaurant.pk)
    else:
        form = MenuItemForm()
    return render(request, "restaurants/menu_item_form.html", {"form": form, "restaurant": restaurant})


@owner_required
def menu_item_edit(request, restaurant_pk, item_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    item = get_object_or_404(MenuItem, pk=item_pk, restaurant=restaurant)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("menu_item_list", restaurant_pk=restaurant.pk)
    else:
        form = MenuItemForm(instance=item)
    return render(request, "restaurants/menu_item_form.html", {"form": form, "restaurant": restaurant})


@owner_required
def menu_item_delete(request, restaurant_pk, item_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    item = get_object_or_404(MenuItem, pk=item_pk, restaurant=restaurant)
    if request.method == "POST":
        item.delete()
        return redirect("menu_item_list", restaurant_pk=restaurant.pk)
    return render(request, "restaurants/menu_item_confirm_delete.html", {"item": item, "restaurant": restaurant})


@owner_required
def owner_orders(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    orders = Order.objects.filter(restaurant=restaurant).order_by("-created_at")
    return render(request, "restaurants/owner_orders.html", {"restaurant": restaurant, "orders": orders})


@owner_required
def update_order_status(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, restaurant__owner=request.user)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return redirect("owner_orders", restaurant_pk=order.restaurant.pk)