from django.contrib import admin

# Register your models here.

from .models import Category, Product, PotravinyFeatures, Comment, CustomUser, Order, OrderLine

# Register your models here
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PotravinyFeatures)
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderLine)
