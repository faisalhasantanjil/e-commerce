from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Tree model
class Tree(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='trees', on_delete=models.CASCADE)
    description = models.TextField()
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def adjust_quantity(self, adjustment):
        if self.quantity + adjustment < 0:
            raise ValidationError("Cannot reduce quantity below zero.")
        self.quantity += adjustment
        self.save()

# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.email = self.user.username
        super().save(*args, **kwargs)
'''
# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        super().save(*args, **kwargs)
'''


# Order item model
class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.tree.name}"
'''
    def get_total_price(self):
        return self.tree.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.pk:
            self.tree.adjust_quantity(-self.quantity)
        else:
            previous_item = OrderItems.objects.get(pk=self.pk)
            quantity_difference = self.quantity - previous_item.quantity
            self.tree.adjust_quantity(-quantity_difference)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.tree.adjust_quantity(self.quantity)
        super().delete(*args, **kwargs)
    '''
# Order model
class Orders(models.Model):
    STATUS = [
        ('Ongoing', 'Ongoing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderItems, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    status= models.CharField(max_length=20, null=True, blank=True, default="Ongoing", choices=STATUS) 

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

