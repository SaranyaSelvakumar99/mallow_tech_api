from django.db import models
from admin_account.models import CustomUser,ProductMaster
# Create your models here.
class BillingMaster(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases',null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    user_paid_cash = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    user_balance_cash = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    class Meta:
        verbose_name = "Billing Master"
        verbose_name_plural = "Billing Master"
        
class DenominationsMaster(models.Model):
    billing = models.ForeignKey(BillingMaster, on_delete=models.CASCADE, related_name='denomination_billing',null=True)
    count_500 = models.IntegerField(default=0)
    count_50 = models.IntegerField(default=0)
    count_20 = models.IntegerField(default=0)
    count_10 = models.IntegerField(default=0)
    count_5 = models.IntegerField(default=0)
    count_2 = models.IntegerField(default=0)
    count_1 = models.IntegerField(default=0)
    is_balance_denomination = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Denomination Master - ID: {self.pk}"
    class Meta:
        verbose_name = "Denomination Master"
        verbose_name_plural = "Denominations Master"
        
class PurchasedItem(models.Model):
    billing = models.ForeignKey(BillingMaster, on_delete=models.CASCADE, related_name='billing',null=True)
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, related_name='purchased_items')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tax_payable_item = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.quantity} x {self.product.name} by {self.customer.email}"
    class Meta:
        verbose_name = "Purchased Item"
        verbose_name_plural = "Purchased Item"