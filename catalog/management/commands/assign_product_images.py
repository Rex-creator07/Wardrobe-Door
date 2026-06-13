from pathlib import Path
from django.conf import settings
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
    help = "Assign proper images to each product from static/images/products/"

    def handle(self, *args, **options):
        images_dir = Path(settings.BASE_DIR) / "static" / "images" / "products"
        updated = 0

        for product_name, filename in PRODUCT_IMAGES.items():
            image_path = images_dir / filename
            if not image_path.exists():
                self.stdout.write(self.style.WARNING(f"Missing image: {filename}"))
                continue

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Product not found: {product_name}"))
                continue

            # FIX: Assign the exact path string relative to your media folder instead of a File upload
            # Matches the exact folder structure Django generated: products/2026/06/filename
            target_path = f"products/2026/06/{filename}"
            
            product.image = target_path
            product.save()

            updated += 1
            self.stdout.write(f"Updated image for: {product_name}")

        self.stdout.write(self.style.SUCCESS(f"Done. {updated} product images updated."))