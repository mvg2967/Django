from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cart.models import Cart, CartItem
from product.models import Product
# Create your views here.
def view(request):
	try:
		the_id = request.session['cart_id']
	except:
		the_id = None
	if the_id:
		cart = Cart.objects.get(id=the_id)
		context_dict = {"cart": cart}
	else:
		empty_message = "Your Cart is Empty, please keep shopping."
		context_dict = {"empty": True, "empty_message": empty_message}
	return render(request, 'cart/view.html', context_dict)

def update_cart(request, slug):
	request.session.set_expiry(120000)
	try:
		qty = request.GET.get('qty')
		update_qty = True
	except:
		qty = None
		update_qty = False

	try:
		attr = request.GET.get('attr')
	except:
		attr = None

	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id

	cart = Cart.objects.get(id=the_id)

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	cart_item = CartItem.objects.get_or_create(cart=cart, product=product)
	if update_qty and qty:
		if int(qty) == 0:
			cart_item.delete()
		else:
			cart_item.quantity=qty
			cart_item.save()
	else:
		pass
	'''
	if not cart_item in cart.items.all():
		cart.items.add(cart_item)
	else:
		cart.items.remove(cart_item)
	'''

	new_total = 0.00
	for item in cart.cartitem_set.all():
		line_total = float(item.product.price) * item.quantity
		new_total += line_total

	request.session['items_total'] = cart.cartitem_set.count()
	cart.total = new_total
	cart.save()

	return HttpResponseRedirect(reverse("view"))