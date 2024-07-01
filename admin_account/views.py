from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductMaster
from .serializers import ProductMasterSerializer
from utils.pagination import pagination_handler

class ProductListCreateAPIView(APIView):
    def get_object(self, pk):
        try:
            return ProductMaster.objects.get(pk=pk)
        except ProductMaster.DoesNotExist:
            return None
        except Exception as e:
            return None
        
    def get(self, request):
        try:
            if "id" in request.query_params:
                id= request.query_params.get('id')
                product = self.get_object(id)
                if product is None:
                    return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = ProductMasterSerializer(product)
                response_data ={'message': 'Product retrieved successfully','product': serializer.data}
            else:
                products = ProductMaster.objects.all()
                page = 1 if not request.query_params.get('page') else request.query_params.get('page')
                limit = 10 if not request.query_params.get('limit') else request.query_params.get('limit')

                res = pagination_handler(len(products),int(page),int(limit))
                result = products[res[0]:res[1]]
                serializer = ProductMasterSerializer(result, many=True)
                response_data = {
                    'message': 'Products retrieved successfully',
                    'total_count': products.count(),
                    'total_count':res[2],
                    'total_page':res[3],
                    'products': serializer.data
                }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'An error occurred while retrieving products','error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            products = request.data
            errors = []
            created_products = []
            for product in products:
                serializer = ProductMasterSerializer(data=product)
                if serializer.is_valid():
                    serializer.save()
                    created_products.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            if errors:
                return Response({'message': 'Some products could not be created', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'All products created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'An error occurred while creating products', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            id = request.query_params.get('id')
            if not id:
                return Response({'message': 'id is required'}, status=status.HTTP_404_NOT_FOUND)
            product = self.get_object(id)
            if not product:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductMasterSerializer(product, data=request.data, context={'product_id': id})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product updated successfully', 'product': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Product update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred while updating the product', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            id = request.query_params.get('id')
            if not id:
                return Response({'message': 'id is required'}, status=status.HTTP_404_NOT_FOUND)
            product = self.get_object(id)
            if not product:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': 'An error occurred while deleting the product', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
