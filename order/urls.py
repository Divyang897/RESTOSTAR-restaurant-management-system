from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.order_home, name='order_home'),
    path('pos_order/', views.pos_order, name='pos_order'),
]
