from django.conf.urls import url,include
from . import views
app_name ='booking'



urlpatterns =[
    
url(r'^$',views.index,name='index'),
url(r'^validation/$',views.validation,name='validation'),
url(r'^reserve/$',views.reserve,name='reserve'),
url(r'^check_reservation/$',views.check_reservation,name='check_reservation'),
url(r'^histogram/$',views.histogram,name='histogram'),
url(r'^delete/$',views.delete,name='delete'),
]   
