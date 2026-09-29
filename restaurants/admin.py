from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem

admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)