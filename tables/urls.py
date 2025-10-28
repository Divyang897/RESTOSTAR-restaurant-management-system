from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.table_home, name='table_home'),
    path('check/', views.check_availability, name='check_availability'),
    path('submit/', views.submit_booking, name='submit_booking'),
    path('booking/today/', views.today_bookings, name='today_bookings'),
    path('tabless/', views.tabless, name='tabless'),
    path('add_tables/', views.add_tables, name='add_tables'),
    path('edit/<int:id>/', views.edit_table, name='edit_table'),
]
