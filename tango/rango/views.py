from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.contrib.auth.models import User


# Create your views here.

def decode_url(mystring):
	return mystring.replace(' ', '_')

def encode_url(mystring):
	return mystring.replace('_',' ')

def index(request):
	# Query the database for a list of ALL a categories currently stored
	# Order the categories by # of likes in descending order
	# Retrieve the top 5 only - or all if less than 5
	# Plave the list in  our context dict dictionary which will be passed to the 
	# template engine
	#request.session.set_test_cookie()
	context = RequestContext(request)
	top_category_list = Category.objects.order_by('-likes')

	for category in top_category_list:
		category.url = encode_url(category.name)
	context_dict = {'categories' : top_category_list}
	category_list = get_category_list()
	
	cat_list = get_category_list()
	context_dict['cat_list']=cat_list

	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	response = render_to_response('rango/index.html', context_dict, context)
	
	# Get the number of visits to the site
	# We use COOKIES.get() function to obtain the visits cookie
	# If the cookie exists the value returned is casted to an integer
	# If the cookie doesn't exist, we default to zero and cast that
	#visits = int(request.COOKIES.get('visits','0'))
	# Does the cookie last_visit exist?
	if request.session.get('last_visit'):
		print("we're in last visit!")
		#last_visit = request.COOKIES['last_visit']
		# Cast the value to a Python date/time object
		last_visit_time = request.session.get('last_visit')#datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		visits = request.session.get('visits', 0)
		# If its been more than a day since the last visit then
		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
			# reassign the value of the cookie to +1 of what it was previously
			response.set_cookie('visits', visits+1)
			request.session['visits'] = visits + 1
			# and update the last visit cookie too
			#response.set_cookie('last_visit', datetime.now())
			#request.session['last_visit'] = str(datetime.now())
	else:
		# cookie last_visit doesn't exist so create it to the current date/time
		response.set_cookie('last_visit', datetime.now())
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
	visits = request.session.get('visits')
	print((visits))
	return response


def about(request):
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0
	context_dict = {'visits' : count}
	return render(request, 'rango/about.html',context_dict)

def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)
	else:
		cat_list = Category.objects.all()

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	for cat in cat_list:
		cat.url = encode_url(cat.name)

	return cat_list

def category(request, category_name_url):
	context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URL's don't handle spaces well, so we encode them as underscores.
	category_name = decode_url(category_name_url)
	print(category_name_url)
	print(category_name)
    # Build up the dictionary we will use as out template context dictionary.
	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	try:
        # Find the category with the given name.
        # Raises an exception if the category doesn't exist.
        # We also do a case insensitive match.
		category = Category.objects.get(name__exact=category_name)
		context_dict['category'] = category
        # Retrieve all the associated pages.
        # Note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
	except Category.DoesNotExist:
        # We get here if the category does not exist.
        # Will trigger the template to display the 'no category' message.
		pass

	if request.method == 'POST':
		query = request.POST.get('query')
		if query:
			query = query.strip()
			result_list = run_query(query)
			context_dict['result_list'] = result_list

    # Go render the response and return it to the client.
	return render_to_response('rango/category.html', context_dict, context)

@login_required
def add_category(request):
	#check for HTTP Post
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#Check for valid form
		if form.is_valid():
			#Save new category to db
			form.save(commit=True)
			#call index() view -> user
			# will be shown homepage
			return index(request)
		else:
			print (form.errors)
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html',{'form':form, 'cat_list' : get_category_list()})

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            try:
                cat = Category.objects.get(name=category_name_url)
                page.category = cat
            except Category.DoesNotExist:
                return render( request, 'rango/add_page.html',context_dict,)
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print (form.errors)
    else:
        form = PageForm()

    return render( request, 'rango/add_page.html',{'category_name_url': category_name_url,
             'category_name': category_name, 'form': form, 'cat_list' : get_category_list()})

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'cat_list' : get_category_list()},
            context)

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your rango account is disabled")
		else:
			print("Invalid log details")
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

def search(request):
	context = RequestContext(request)    
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			result_list = run_query(query)

	return render_to_response('rango/search.html', {'result_list' : result_list}, context)

@login_required
def profile(request):
	context = RequestContext(request)
	cat_list = get_category_list()
	context_dict = {'cat_list':cat_list}
	u = User.objects.get(username=request.user)
	try:
		up = UserProfile.objects.get(user=u)
	except:
		up = None

	context_dict['user'] = u
	context_dict['userprofile'] = up
	return render_to_response('rango/profile.html', context_dict, context)

def track_url(request):
	context = RequestContext(request)
	page_id = None
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views+1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)

def like_category(request):
	context = RequestContext(request)
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']

	likes = 0
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		if category:
			likes = category.likes + 1
			category.likes = likes
			category.save()
	print(likes)
	return HttpResponse(likes)

def suggest_category(request):
	context = RequestContext(request)
	cat_list = []
	starts_with = ''
	if request.GET == 'GET':
		starts_with = request.GET['suggestion']
	cat_list = get_category_list(8, starts_with)
	return render_to_response('rango/category_list.html', {'cat_list' : cat_list}, context)

@login_required
def auto_add_page(request):
    context = RequestContext(request)
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)

            pages = Page.objects.filter(category=category).order_by('-views')

            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
    print("in auto add page")
    return render_to_response('rango/page_list.html', context_dict, context)
