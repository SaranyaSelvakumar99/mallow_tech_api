from rest_framework import serializers
from admin_account.models import CustomUser
from .models import PurchasedItem,DenominationsMaster,BillingMaster

# from django.db.models import Q
class PurchasedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItem
        fields = '__all__'
    def to_representation(self, instance):
        primitive_repr = super(PurchasedItemSerializer, self).to_representation(instance)
        primitive_repr['total_price_with_tax_'] = instance.tax_payable_item + instance.total_item_price
        return primitive_repr
    
class DenominationsMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DenominationsMaster
        fields = '__all__'
        
class BillingMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingMaster
        fields = '__all__'
        
    def to_representation(self, instance):
        primitive_repr = super(BillingMasterSerializer, self).to_representation(instance)
        primitive_repr['email'] = CustomUser.objects.get(id=instance.customer_id).email
        total_price_with_tax = instance.total_price + instance.total_tax
        primitive_repr['total_price_without_tax'] = instance.total_price
        primitive_repr['total_tax_payable'] = instance.total_tax
        primitive_repr['net_price_purchased_item'] = total_price_with_tax
        primitive_repr['round_price_purchased_item'] = round(total_price_with_tax)  # Assuming you want to round to nearest integer
        primitive_repr['balance_payable_to_user'] = instance.user_paid_cash - total_price_with_tax
        purchased_products = PurchasedItem.objects.filter(billing_id=instance.id)
        primitive_repr['purchased_products'] = PurchasedItemSerializer(purchased_products,many=True).data
        
        return primitive_repr