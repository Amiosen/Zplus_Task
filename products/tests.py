from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product

class ProductsAPITestCase(APITestCase):
    def setUp(self):
        Product.objects.create(
            title="Product 1",
            price=100.00,
            description="Test description 1",
            category="Category 1",
            stock_status="In Stock",
            image_urls=["https://example.com/image1.jpg"],
            image_directory="dir1",
        )
        Product.objects.create(
            title="Product 2",
            price=200.00,
            description="Test description 2",
            category="Category 2",
            stock_status="Out of Stock",
            image_urls=["https://example.com/image2.jpg"],
            image_directory="dir2",
        )
        self.url = reverse("product-list")

    def test_get_products_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIn("total_pages", response.data)
        self.assertIn("current_page", response.data)
        self.assertIn("page_size", response.data)
        self.assertIn("total_items", response.data)
