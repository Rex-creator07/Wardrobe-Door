from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("ajax/add-to-cart/", views.AddToCartView.as_view(), name="add_to_cart"),
]
