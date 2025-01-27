# Generated by Django 5.0.6 on 2024-06-28 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DenominationsMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_500', models.IntegerField(default=0)),
                ('count_50', models.IntegerField(default=0)),
                ('count_20', models.IntegerField(default=0)),
                ('count_10', models.IntegerField(default=0)),
                ('count_5', models.IntegerField(default=0)),
                ('count_2', models.IntegerField(default=0)),
                ('count_1', models.IntegerField(default=0)),
                ('is_balance_denomination', models.BooleanField(default=False)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Denomination Master',
                'verbose_name_plural': 'Denominations Master',
            },
        ),
    ]
