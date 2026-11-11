from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(help_text="Price in rupees")

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    customer = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["customer", "product"], name="one_product_per_customer"),
        ]
