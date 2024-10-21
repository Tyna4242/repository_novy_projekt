

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Fixed discount
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage discount
    expiration_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=1)  # Maximum number of times it can be used
    times_used = models.PositiveIntegerField(default=0)

    def is_valid(self):
        if self.expiration_date and timezone.now() > self.expiration_date:
            return False
        if self.times_used >= self.usage_limit:
            return False
        return self.active

    def apply_discount(self, total_cost):
        """Apply either a percentage or fixed discount"""
        total_cost_decimal = Decimal(total_cost)
        if self.discount_percent > 0:
            discount_amount = total_cost_decimal * (Decimal(self.discount_percent) / Decimal(100))
            return total_cost_decimal - discount_amount
        elif self.discount_amount > 0:
            return max(total_cost_decimal - Decimal(self.discount_amount), Decimal(0))
        return total_cost_decimal

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% or {self.discount_amount} fixed discount"


class CustomUser(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Role field: ADMIN or USER
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    # Preferred communication channel: mail or email
    COMMUNICATION_CHOICES = [
        ('mail', 'Mail'),
        ('email', 'Email'),
    ]
    preferred_communication = models.CharField(max_length=10, choices=COMMUNICATION_CHOICES, default='email')



    
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    

class PotravinyFeatures(models.Model):
    feature_name = models.CharField(max_length=225)

    def __str__(self):
        return self.feature_name

    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('l', 'Liter'), ('ml', 'Milliliter')])
    features = models.ManyToManyField(PotravinyFeatures)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    promo_code = models.CharField(max_length=50, null=True, blank=True)  # Track promo code used


    def calculate_total_cost(self):
        return sum(line.get_line_total() for line in self.order_lines.all())

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.total_cost = self.calculate_total_cost()


class OrderLine(models.Model):
    order = models.ForeignKey(Order, related_name='order_lines', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} at {self.price}"