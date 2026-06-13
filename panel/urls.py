from django.urls import path

from panel import views

app_name = "panel"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/add/", views.ProductFormView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", views.ProductFormView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/status/", views.OrderStatusUpdateView.as_view(), name="order_status"),
    path("users/", views.UserListView.as_view(), name="users"),
]
