

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


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

