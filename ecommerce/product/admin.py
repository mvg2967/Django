from django.contrib import admin
from product.models import Product, ProductImage
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
	exclude = ['timestamp']
	prepopulated_fields = {'slug':('title',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)