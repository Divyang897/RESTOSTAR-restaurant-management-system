from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_home, name='menu_home'),
    path('categories/', views.category_home, name='category_home'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    path('edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('today-special/', views.today_special, name='today-special'),
    path('save-today-special/', views.save_today_special, name='save_today_special'),
    path('save-dropped-special/', views.save_scheduled_special, name='save_scheduled_special'),
    path('get_scheduled_specials/', views.get_scheduled_specials, name='get_scheduled_specials'),
    path('delete_scheduled_special/', views.delete_scheduled_special, name='delete_scheduled_special'),
    path('delete_special/<int:special_id>/', views.delete_special, name='delete_special'),
    path('delete_menu_item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
]   
