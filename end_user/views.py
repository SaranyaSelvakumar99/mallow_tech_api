from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from admin_account import *
from .models import *
from .serializers import *
import requests
from django.shortcuts import render
import json
from django.http import JsonResponse
from utils.helper import send_custom_mail, sum_of_denomination

# Create your views here.
class UserBillingAPIView(APIView):
    def get(self, request):
        try:
            id = request.query_params.get('id')
            if not id:
                return Response({'message': 'Billing id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            billing_products = BillingMaster.objects.filter(id=id)
            if not billing_products.exists():
                return Response({'message': 'Billing product not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BillingMasterSerializer(billing_products, many=True)
            return Response({'message': 'Billing product retrieved successfully', 'billing_product': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': 'An error occurred while retrieving billing products',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request):
        try:
            request_data = request.data
            errors = []
            purchased_items = []
            total_item_price_sum = 0.0
            tax_payable_item = 0.0
            
            if not request_data.get('products') or not request_data.get('email'):
                return Response({'message': 'Products and email are required'}, status=status.HTTP_400_BAD_REQUEST)

            denominations = sum_of_denomination(request_data)
            total_cash = sum(denom * count for denom, count in denominations.items())
            if int(request_data['user_paid_cash']) < total_cash:
                return Response({'error': 'User-paid cash must be greater than or equal to total cash bb'}, status=status.HTTP_400_BAD_REQUEST)
            
            #validation - product quantity  
            for req in request_data['products']:
                product_obj = ProductMaster.objects.get(id=req['product_id'])
                if product_obj.stock_quantity < req['quantity']:
                    errors.append({'product_id': product_obj.id, 'error': 'Insufficient stock'})
                    continue
                
            user, _ = CustomUser.objects.get_or_create(email=request_data['email'])
            billing_obj = BillingMaster.objects.create(customer=user)
            
            for req in request_data['products']:
                product_obj = ProductMaster.objects.get(id=req['product_id'])
                req.update({
                    'billing': billing_obj.id,
                    'product': req['product_id'],
                    'unit_price': float(product_obj.price),
                    'purchase_price': float(product_obj.price),
                    'tax_percentage': float(product_obj.tax_percentage),
                    'tax_payable_item': (float(product_obj.price) * float(product_obj.tax_percentage) / 100)*req['quantity'],
                    'total_item_price': float(product_obj.price) * req['quantity']
                })

                serializer = PurchasedItemSerializer(data=req)
                if serializer.is_valid():
                    serializer.save()
                    purchased_items.append(serializer.data)
                    product_obj.stock_quantity -= req['quantity']
                    product_obj.save()
                    total_item_price_sum += req['total_item_price']
                    tax_payable_item += req['tax_payable_item']
                else:
                    errors.append(serializer.errors)
            #billing info update
            billing_obj.total_price = total_item_price_sum
            billing_obj.total_tax = tax_payable_item
            billing_obj.user_paid_cash = request_data.get('user_paid_cash', 0.0)
            billing_obj.save()
            #denomination creation
            request_data['billing'] = billing_obj.id
            denom_serializer = DenominationsMasterSerializer(data=request_data)
            if denom_serializer.is_valid():
                denom_serializer.save()
            else:
                errors.append(denom_serializer.errors)

            if errors:
                return Response({
                    'message': 'Some products could not be purchased',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # #billing_serializer-email
            billing_products=BillingMaster.objects.filter(id=billing_obj.id)
            serializer = BillingMasterSerializer(billing_products,many=True).data
            data  = {"billing_product":serializer}
            context={'data': data, 'email': request_data['email']}
            send_custom_mail(context, request_data['email'], "Billing Details", 'billing2.html')
            
            return Response({
                'message': f'All products purchased successfully and email sent your account {billing_obj.id}'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': 'An error occurred while billing products',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
# ----template view functions------------
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def generate_bill(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user_paid_cash_str = request.POST.get('user_paid_cash', '0.00')
        try:
            user_paid_cash = float(user_paid_cash_str)
        except ValueError:
            user_paid_cash = 0.00

        products = []
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        for product_id, quantity in zip(product_ids, quantities):
            if product_id and quantity:  # Check if both product_id and quantity are present
                products.append({
                    "product_id": int(product_id),
                    "quantity": int(quantity)
                })
         
        payload = {
            "email": email,
            "products":products,
            "count_500": int(request.POST.get('count_500', '0')),
            "count_50": int(request.POST.get('count_50', '0')),
            "count_20": int(request.POST.get('count_20', '0')),
            "count_10": int(request.POST.get('count_10', '0')),
            "count_5": int(request.POST.get('count_5', '0')),
            "count_2": int(request.POST.get('count_2', '0')),
            "count_1": int(request.POST.get('count_1', '0')),
            "user_paid_cash": user_paid_cash
        }
        json_payload = json.dumps(payload)
        api_endpoint = 'http://127.0.0.1:8000/mallotech_user/api/user_billing/'
        headers = {
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(api_endpoint, data=json_payload, headers=headers)
            response_data = response.json()
            return JsonResponse(response_data)  
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)  

    return render(request, 'billing1.html')

def billing_page(request,id):
    response = requests.get(f'http://127.0.0.1:8000/mallotech_user/api/user_billing/?id={id}')
    data = response.json()
    email = data.get('email', '')
    return render(request, 'billing2.html', {'data': data, 'email': email})
