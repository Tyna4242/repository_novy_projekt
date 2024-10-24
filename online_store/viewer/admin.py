from django.contrib import admin

# Register your models here.

from .models import Category, Product, PotravinyFeatures, Comment, CustomUser, Order, OrderLine, PromoCode
from django.contrib import admin

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'discount_percent', 'expiration_date', 'active', 'usage_limit', 'times_used')
    search_fields = ('code',)
    list_filter = ('active', 'expiration_date')


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PotravinyFeatures)
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderLine)
