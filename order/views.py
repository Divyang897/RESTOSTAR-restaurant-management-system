from django.shortcuts import render
from menu.models import MenuItem  # <-- Import your model

# Create your views here.
def order_home(request):
    return render(request, 'order/order_home.html')


def pos_order(request):
    # Fetch all menu items from the database
    menu_items = MenuItem.objects.all().order_by('category', 'name')

    # Pass them to the template
    return render(request, 'order/order_pos.html', {'menu_items': menu_items})