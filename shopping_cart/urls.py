from django.urls import path

from shopping_cart import views

app_name = "shopping_cart"

urlpatterns = [
    path("", views.CartView.as_view(), name="cart"),
    path("remove/<int:product_id>/", views.RemoveFromCartView.as_view(), name="remove"),
    path("clear/", views.ClearCartView.as_view(), name="clear"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]
