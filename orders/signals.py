from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created or not instance.email:
        return
    send_mail(
        subject="Welcome to The Wardrobe Door",
        message=(
            f"Hi {instance.username},\n\n"
            "Welcome to The Wardrobe Door! Your account has been created successfully.\n\n"
            "Start shopping our latest collections today.\n\n"
            "— The Wardrobe Door Team"
        ),
        from_email=None,
        recipient_list=[instance.email],
        fail_silently=True,
    )


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if not created:
        return
    items = instance.items.select_related("product")
    lines = [
        f"- {item.product.name} x{item.quantity} @ ${item.price} = ${item.line_total()}"
        for item in items
    ]
    body = (
        f"Hi {instance.full_name},\n\n"
        f"Thank you for your order #{instance.pk}!\n\n"
        "Items:\n"
        f"{chr(10).join(lines)}\n\n"
        f"Total: ${instance.total_amount}\n"
        f"Status: {instance.get_status_display()}\n\n"
        "Shipping to:\n"
        f"{instance.address}\n"
        f"{instance.city}, {instance.state} {instance.zip_code}\n\n"
        "— The Wardrobe Door Team"
    )
    send_mail(
        subject=f"Order Confirmation #{instance.pk} - The Wardrobe Door",
        message=body,
        from_email=None,
        recipient_list=[instance.email],
        fail_silently=True,
    )
