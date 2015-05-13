from django.db import models
from django.template import RequestContext
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	views = models.IntegerField(default = 0, unique=False)
	likes = models.IntegerField(default = 0,unique=False)
	
	def __str__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default = 0,unique=False)

	def __str__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	websites = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username