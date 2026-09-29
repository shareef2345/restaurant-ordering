from django.shortcuts import get_object_or_404, render

from .models import Restaurant


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