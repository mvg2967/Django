from django.db import models

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=100)
	slug = models.SlugField()
	timestamp = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_price(self):
		return self.title

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='images/products/')
	thumbnail = models.BooleanField(default=False)

	def __str__(self):
		return self.product.title