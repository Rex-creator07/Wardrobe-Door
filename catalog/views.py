from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views import View

from catalog.models import Product


def get_category_header_image(category="", subcategory=""):
    images = {
        "men": {
            "default": "images/headers/mens-collection.jpg",
            "upper": "images/headers/mens-upper.jpg",
            "torso": "images/headers/mens-torso.jpg",
            "footwear": "images/headers/mens-footwear.jpg",
        },
        "women": {
            "default": "images/headers/womens-collection.jpg",
            "upper": "images/headers/womens-upper.jpg",
            "torso": "images/headers/womens-torso.jpg",
            "footwear": "images/headers/womens-footwear.jpg",
        },
        "default": "images/headers/all-products.jpg",
    }
    if category and category in images:
        if subcategory and subcategory in images[category]:
            return images[category][subcategory]
        return images[category]["default"]
    return images["default"]


class HomeView(View):
    def get(self, request):
        featured = Product.objects.order_by("?")[:4]
        return render(request, "catalog/home.html", {"featured_products": featured})


class ProductListView(View):
    def get(self, request):
        category = request.GET.get("category", "")
        subcategory = request.GET.get("subcategory", "")
        sort = request.GET.get("sort", "newest")

        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if subcategory:
            products = products.filter(sub_category=subcategory)

        sort_map = {
            "price-low": "price",
            "price-high": "-price",
            "name": "name",
            "newest": "-created_at",
        }
        products = products.order_by(sort_map.get(sort, "-created_at"))

        page_title = "All Products"
        page_description = "Discover our latest collection of high-quality clothing."
        if category:
            page_title = category.capitalize()
            if subcategory:
                page_title += f" {subcategory.capitalize()}"
                page_description = (
                    f"Explore our collection of {category} {subcategory} wear."
                )
            else:
                page_description = f"Browse our complete collection of {category} clothing."
            page_title += " Collection"

        return render(
            request,
            "catalog/products.html",
            {
                "products": products,
                "category": category,
                "subcategory": subcategory,
                "sort": sort,
                "page_title": page_title,
                "page_description": page_description,
                "header_image": get_category_header_image(category, subcategory),
            },
        )


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        related = (
            Product.objects.filter(
                category=product.category, sub_category=product.sub_category
            )
            .exclude(pk=product.pk)
            .order_by("?")[:4]
        )
        return render(
            request,
            "catalog/product_detail.html",
            {"product": product, "related_products": related},
        )

    def post(self, request, pk):
        from django.contrib import messages
        from django.shortcuts import redirect
        from shopping_cart.cart import Cart

        product = get_object_or_404(Product, pk=pk)
        quantity = max(1, int(request.POST.get("quantity", 1)))
        cart = Cart(request)
        cart.add(product, quantity)
        messages.success(request, "Product added to cart")
        return redirect("shopping_cart:cart")


class AddToCartView(View):
    def post(self, request):
        from django.http import JsonResponse
        from django.shortcuts import get_object_or_404
        from shopping_cart.cart import Cart

        product = get_object_or_404(Product, pk=request.POST.get("product_id"))
        quantity = max(1, int(request.POST.get("quantity", 1)))
        cart = Cart(request)
        cart.add(product, quantity)
        return JsonResponse(
            {
                "success": True,
                "message": "Product added to cart",
                "cart_count": len(cart),
            }
        )
