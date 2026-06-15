from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from catalog.models import Product

User = get_user_model()

SAMPLE_PRODUCTS = [
    ("Men's Classic Suit", "men", "torso", 299.99, "A stylish classic suit for men", "mens_suit.jpg"),
    ("Men's Casual Jacket", "men", "upper", 89.99, "A comfortable casual jacket for men", "mens_jacket.jpg"),
    ("Men's Leather Shoes", "men", "footwear", 129.99, "Classic leather shoes for men", "mens_shoes.jpg"),
    ("Women's Summer Dress", "women", "torso", 79.99, "A beautiful summer dress for women", "womens_dress.jpg"),
    ("Women's Designer Bag", "women", "upper", 59.99, "A stylish designer bag for women", "womens_bag.jpg"),
    ("Women's High Heels", "women", "footwear", 99.99, "Elegant high heels for women", "womens_heels.jpg"),
]


class Command(BaseCommand):
    help = "Create demo admin user and sample products"

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user created (admin / admin123)"))
        else:
            admin.is_staff = True
            admin.is_superuser = True
            admin.set_password("admin123")
            admin.save()
            self.stdout.write("Admin user updated (admin / admin123)")

        if Product.objects.exists():
            self.stdout.write("Products already exist, skipping seed.")
            from django.core.management import call_command
            call_command("assign_product_images")
            call_command("setup_site")
            return

        for name, category, sub_category, price, description, image_file in SAMPLE_PRODUCTS:
            Product.objects.create(
                name=name,
                category=category,
                sub_category=sub_category,
                price=price,
                description=description,
                image=f"images/products/{image_file}",
            )
            self.stdout.write(f"Created product: {name}")

        self.stdout.write(self.style.SUCCESS("Demo data setup complete."))

        from django.core.management import call_command
        call_command("setup_site")
