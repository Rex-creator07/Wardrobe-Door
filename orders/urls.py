from django.urls import path

from shopping_cart.views import OrderConfirmationView

app_name = "orders"

urlpatterns = [
    path("confirmation/<int:pk>/", OrderConfirmationView.as_view(), name="confirmation"),
]
