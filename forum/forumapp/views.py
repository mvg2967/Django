from django.shortcuts import render
from django.http import HttpResponse
from forumapp.models import Forum, Post, Thread, UserProfile

# Create your views here.
def index(request):
	forums = Forum.objects.all()
	for forum in forums:
		print(forum.title)
		print(forum.num_posts())
		print(forum.last_post())
	return render(request, 'forumapp/forums.html', {'forums':forums})