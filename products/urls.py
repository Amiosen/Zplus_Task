from django.urls import path
from .apis import ProductsAPI

urlpatterns = [
    path('api/products/', ProductsAPI.as_view(), name='product-list'),
]
