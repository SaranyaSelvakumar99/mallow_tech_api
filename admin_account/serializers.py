from rest_framework import serializers
from .models import ProductMaster
from django.db.models import Q
class ProductMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaster
        fields = '__all__'

    def validate_product_name(self, value):
        product_id = self.context.get('product_id')
        print(product_id,"_____")
        # if ProductMaster.objects.filter(~Q(id=product_id),product_name=value).exists():
        #     raise serializers.ValidationError(f"{value} product with this name already exists.")
        if ProductMaster.objects.filter(product_name=value).exists():
            raise serializers.ValidationError(f"{value} product with this name already exists.")
        return value
