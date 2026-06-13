from decimal import Decimal

from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("wardrobe_cart")
        if cart is None:
            cart = self.session["wardrobe_cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]["quantity"] = quantity
            else:
                self.remove(product_id)
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["wardrobe_cart"] = {}
        self.cart = self.session["wardrobe_cart"]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for product_id, item in self.cart.items():
            product = product_map.get(product_id)
            if not product:
                continue
            yield {
                "product": product,
                "quantity": item["quantity"],
                "price": Decimal(item["price"]),
                "subtotal": Decimal(item["price"]) * item["quantity"],
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def is_empty(self):
        return len(self.cart) == 0
