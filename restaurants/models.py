from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    CUISINE_IMAGES = {
    "italian": "https://images.unsplash.com/photo-1595854341625-f33ee10dbf94?w=500",
    "chinese": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500",
    "indian": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500",
    "mexican": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500",
    "dosa": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500",
    "pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500",
    "burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500",
    }
    DEFAULT_IMAGE = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500"

    def get_image_url(self):
        return self.CUISINE_IMAGES.get(self.cuisine.strip().lower(), self.DEFAULT_IMAGE)
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menu_items"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Order(models.Model):
    STATUS_CHOICES = (
        ("PLACED", "Placed"),
        ("PREPARING", "Preparing"),
        ("DELIVERED", "Delivered"),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PLACED"
    )
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

