from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from catalog.models import Product
from orders.models import Order, OrderItem
from shopping_cart.cart import Cart


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "shopping_cart/cart.html", {"cart": cart})

    def post(self, request):
        cart = Cart(request)
        if "update_cart" in request.POST:
            for key, quantity in request.POST.items():
                if key.startswith("quantity_"):
                    pid = key.replace("quantity_", "")
                    cart.update(pid, max(1, int(quantity)))
            messages.success(request, "Cart updated successfully")
        return redirect("shopping_cart:cart")


class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        messages.success(request, "Item removed from cart")
        return redirect("shopping_cart:cart")


class ClearCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        messages.success(request, "Cart cleared")
        return redirect("shopping_cart:cart")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.error(request, "Your cart is empty")
            return redirect("shopping_cart:cart")
        return render(request, "shopping_cart/checkout.html", {"cart": cart})

    def post(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.error(request, "Your cart is empty")
            return redirect("shopping_cart:cart")

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        zip_code = request.POST.get("zip", "").strip()
        phone = request.POST.get("phone", "").strip()

        errors = []
        if not full_name:
            errors.append("Full name is required")
        if not email:
            errors.append("Valid email is required")
        if not address:
            errors.append("Address is required")
        if not city:
            errors.append("City is required")
        if not state:
            errors.append("State is required")
        if not zip_code:
            errors.append("ZIP code is required")
        if not phone:
            errors.append("Phone number is required")

        if errors:
            messages.error(request, " ".join(errors))
            return render(request, "shopping_cart/checkout.html", {"cart": cart})

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.get_total(),
                    full_name=full_name,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    phone=phone,
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        quantity=item["quantity"],
                        price=item["price"],
                    )
                cart.clear()
        except Exception as exc:
            messages.error(request, f"Error processing order: {exc}")
            return render(request, "shopping_cart/checkout.html", {"cart": cart})

        messages.success(
            request, f"Order placed successfully! Your order number is {order.pk}"
        )
        return redirect("orders:confirmation", pk=order.pk)


class OrderConfirmationView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        return render(request, "orders/confirmation.html", {"order": order})
