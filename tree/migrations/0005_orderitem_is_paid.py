# Generated by Django 5.0.6 on 2024-09-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tree", "0004_order_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="is_paid",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
