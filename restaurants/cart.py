from decimal import Decimal

from .models import MenuItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1):
        item_id = str(menu_item.id)
        if item_id in self.cart:
            self.cart[item_id]["quantity"] += quantity
        else:
            self.cart[item_id] = {
                "quantity": quantity,
                "price": str(menu_item.price),
                "restaurant_id": menu_item.restaurant_id,
            }
        self.save()

    def remove(self, menu_item_id):
        item_id = str(menu_item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        menu_items = MenuItem.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in menu_items:
            cart[str(item.id)]["menu_item"] = item

        for item_id, item_data in cart.items():
            item_data["total_price"] = Decimal(item_data["price"]) * item_data["quantity"]
            yield item_data

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())