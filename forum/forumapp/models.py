from django.db import models
from django.contrib.auth.models import User
from forum.settings import MEDIA_URL

# Create your models here.
class Forum(models.Model):
	title = models.CharField(max_length=60)

	def __str__(self):
		return self.title

	def num_posts(self):
		i = 0
		#return sum([t.num_posts() for t in self.thread_set.all()])
		for t in self.thread_set.all():
			i += 1
		return i

	def last_post(self):
		if self.thread_set.count():
			last = None
			for t in self.thread_set.all():
				l = t.last_post()
				if l:
					if not last: 
						last = l
					elif l.created > last.created: 
						last = l
			return last

class Thread(models.Model):
	title = models.CharField(max_length=60)
	created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User)
	forum = models.ForeignKey(Forum)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return str("%s - %s" % (self.creator, self.title))

	def last_post(self):
		if self.post_set.count():
			return self.post_set.order_by("created")[0]

class Post(models.Model):
	title = models.CharField(max_length=60)
	created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User)
	thread = models.ForeignKey(Thread)
	body = models.TextField(max_length=10000)

	class Meta:
		ordering = ["created"]

	def __str__(self):
		return "%s - %s - %s" % (self.creator, self.thread, self.title)

	def profile_date(self):
		p = self.creator.profile
		return p.posts, p.avatar

class UserProfile(models.Model):
	avatar = models.ImageField("Profile Pic", upload_to="images/",blank=True, null=True)
	posts = models.IntegerField(default=0)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.user

	def increment_posts(self):
		self.posts += 1
		self.save()

	def avatar_image(self):
		return (MEDIA_URL + self.avatar.name) if self.avatar else None
