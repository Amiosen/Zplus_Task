from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .pagination import ProductsPagination
from .models import Product
from .serializers import ProductOutputSerializer


class ProductsAPI(APIView):
    @extend_schema(
        responses=ProductOutputSerializer,
        summary="Return all crawled products",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description="Items Page number",
                required=False,
                type=int,
            ),
        ]
    )
    def get(self, request):
        queryset = Product.objects.all()
        paginator = ProductsPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        serializer = ProductOutputSerializer(
            paginated_queryset,
            many=True,
        )
        return Response(
            {
                "results": serializer.data,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "page_size" : paginator.page.paginator.per_page,
                "total_items" : paginator.page.paginator.count,
            },
            status=status.HTTP_200_OK,
        )