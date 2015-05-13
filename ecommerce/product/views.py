from django.shortcuts import render
from product.models import Product
# Create your views here.
def index(request):
	products = Product.objects.all()
	context_dict = {'products':products}
	return render(request,'product/index.html',context_dict)

def view_product(request, slug):
	product = Product.objects.get(slug=slug)
	context_dict = {'product':product}
	return render(request,'product/view_product.html',context_dict)

def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			result_list = Product.objects.filter(title__icontains=query)
	return render(request,'product/search.html',{'result_list':result_list})