from django.core.management.base import BaseCommand
from catalog.models import Product

PRODUCT_IMAGES = {
    "Men's Classic Suit": "mens_suit.jpg",
    "Men's Casual Jacket": "mens_jacket.jpg",
    "Men's Leather Shoes": "mens_shoes.jpg",
    "Women's Summer Dress": "womens_dress.jpg",
    "Women's Designer Bag": "womens_bag.jpg",
    "Women's High Heels": "womens_heels.jpg",
}

class Command(BaseCommand):
    help = "Link products directly to tracked media assets"

    def handle(self, *args, **options):
        updated = 0

        for product_name, filename in PRODUCT_IMAGES.items():
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Product not found: {product_name}"))
                continue

            # Directly point the database record to the tracked folder path
            # This stops Django from appending random strings like _bC5...
            product.image = f"products/2026/06/{filename}"
            product.save()

            updated += 1
            self.stdout.write(f"Linked image path for: {product_name}")

        self.stdout.write(self.style.SUCCESS(f"Done. {updated} paths synchronized."))