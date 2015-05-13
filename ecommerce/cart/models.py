from django.db import models
from product.models import Product

# Create your models here.
class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=1)
	timestamp = models.DateField(auto_now_add=True)
	line_total = models.DecimalField(default=10.99,max_digits=1000, decimal_places=2)
	def __str__(self):
		try:
			return str(self.cart.id)
		except:
			return self.product.title

class Cart(models.Model):
	#items = models.ManyToManyField(CartItem, null=True, blank=True)
	#products = models.ManyToManyField(Product, null=True, blank=True)
	total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
	timestamp = models.DateField(auto_now_add=True)

	def __str__(self):
		return "Cart id: " + str(self.id)