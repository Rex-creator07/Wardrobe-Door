from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from catalog.models import Product
from orders.models import Order

User = get_user_model()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_count"] = Product.objects.count()
        context["order_count"] = Order.objects.count()
        context["user_count"] = User.objects.filter(is_staff=False).count()
        context["total_revenue"] = (
            Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0
        )
        context["recent_orders"] = Order.objects.select_related("user")[:5]
        return context


class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = "panel/products.html"
    context_object_name = "products"
    ordering = ["name"]


class ProductFormView(StaffRequiredMixin, View):
    template_name = "panel/product_form.html"

    def get(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk) if pk else None
        return render(
            request,
            self.template_name,
            {"product": product, "edit_mode": bool(product)},
        )

    def post(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk) if pk else None
        name = request.POST.get("name", "").strip()
        category = request.POST.get("category", Product.CATEGORY_MEN)
        sub_category = request.POST.get("sub_category", Product.SUB_UPPER)
        price = request.POST.get("price", "0")
        description = request.POST.get("description", "").strip()
        image_path = request.POST.get("image", "").strip()

        errors = []
        if not name:
            errors.append("Product name is required")
        try:
            price = float(price)
            if price <= 0:
                errors.append("Price must be greater than zero")
        except ValueError:
            errors.append("Invalid price")

        if errors:
            messages.error(request, " ".join(errors))
            return render(
                request,
                self.template_name,
                {"product": product, "edit_mode": bool(product)},
            )

        if product:
            product.name = name
            product.category = category
            product.sub_category = sub_category
            product.price = price
            product.description = description
            if image_path:
                product.image = image_path
            product.save()
            messages.success(request, "Product updated successfully")
        else:
            if not image_path:
                messages.error(request, "Product image path is required")
                return render(
                    request, self.template_name, {"product": None, "edit_mode": False}
                )
            Product.objects.create(
                name=name,
                category=category,
                sub_category=sub_category,
                price=price,
                description=description,
                image=image_path,
            )
            messages.success(request, "Product created successfully")
        return redirect("panel:products")


class ProductDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("panel:products")


class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "panel/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("user").prefetch_related("items__product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Order.STATUS_CHOICES
        return context


class OrderStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status = request.POST.get("status")
        valid_statuses = dict(Order.STATUS_CHOICES)
        if status in valid_statuses:
            order.status = status
            order.save()
            messages.success(request, f"Order #{order.pk} status updated")
        return redirect("panel:orders")


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = "panel/users.html"
    context_object_name = "users"
    queryset = User.objects.order_by("-date_joined")
