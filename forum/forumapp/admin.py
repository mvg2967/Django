from django.contrib import admin
from forumapp.models import Forum, Thread, Post, UserProfile
# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
	list_display = ['title', 'forum', 'creator', 'created']
	list_filter = ['forum', 'creator']

class PostAdmin(admin.ModelAdmin):
	search_fields = ['title', 'creator']
	list_display = ['title', 'thread', 'creator', 'created']

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user']

def create_user_profile(sender, **kwargs):
	user = kwargs['instance']
	if not UserProfile.objects.filter(user=user):
		UserProfile(user=user).save()

admin.site.register(Forum)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, ProfileAdmin)