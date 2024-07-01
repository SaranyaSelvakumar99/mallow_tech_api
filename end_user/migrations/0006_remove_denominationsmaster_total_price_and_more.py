# Generated by Django 5.0.6 on 2024-06-29 06:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('end_user', '0005_denominationsmaster_user_paid_cash'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denominationsmaster',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='denominationsmaster',
            name='user',
        ),
        migrations.RemoveField(
            model_name='denominationsmaster',
            name='user_paid_cash',
        ),
        migrations.RemoveField(
            model_name='purchaseditem',
            name='customer',
        ),
        migrations.CreateModel(
            name='BillingMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('user_paid_cash', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('user_balance_cash', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Billing Master',
                'verbose_name_plural': 'Billing Master',
            },
        ),
        migrations.AddField(
            model_name='denominationsmaster',
            name='billing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='denomination_billing', to='end_user.billingmaster'),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='billing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing', to='end_user.billingmaster'),
        ),
    ]
