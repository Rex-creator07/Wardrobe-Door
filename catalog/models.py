from django.db import models


class Product(models.Model):
    CATEGORY_MEN = "men"
    CATEGORY_WOMEN = "women"
    CATEGORY_CHOICES = [
        (CATEGORY_MEN, "Men"),
        (CATEGORY_WOMEN, "Women"),
    ]

    SUB_UPPER = "upper"
    SUB_TORSO = "torso"
    SUB_FOOTWEAR = "footwear"
    SUB_CATEGORY_CHOICES = [
        (SUB_UPPER, "Upper"),
        (SUB_TORSO, "Torso"),
        (SUB_FOOTWEAR, "Footwear"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=10, choices=SUB_CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/%Y/%m/")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
