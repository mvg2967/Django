from django.conf.urls import patterns, url
from product import views

urlpatterns = patterns('',
	url(r'^$',views.index, name='index'),
	url(r'^view_product/(?P<slug>[^\.]+)/$',views.view_product,name='view_product'),
	url(r'^search/$',views.search, name='search'),
	)