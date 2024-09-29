# Generated by Django 5.0.6 on 2024-07-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tree", "0002_order_delivery_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
