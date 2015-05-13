from django.conf.urls import patterns, url
from cart import views

urlpatterns = patterns('',
	url(r'^$',views.view, name='view'),
	url(r'^update/(?P<slug>[^\.]+)/$',views.update_cart,name='update_cart'),
)
