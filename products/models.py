from django.db import models



class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    stock_status = models.CharField(max_length=100, blank=True, null=True)
    image_urls = models.JSONField(default=list)

    def __str__(self):
        return self.title
