# Generated by Django 5.0.6 on 2024-06-28 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('end_user', '0003_rename_user_id_denominationsmaster_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseditem',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='tax_payable_item',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='total_item_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
