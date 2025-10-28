import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem, Category,MenuItem, TodaySpecial,ScheduledSpecial, TodaySpecial

@login_required(login_url='/login/')
def menu_home(request):
    # Fetch all menu items
    menu_items = MenuItem.objects.select_related('category').all()
    # Fetch all categories for dropdown
    categories = Category.objects.all()
    return render(request, 'menu/display.html', {
        'menu_items': menu_items,
        'categories': categories  # <-- send this to template
    })
def category_home(request):
    # Fetch all categories
    categories = Category.objects.all()
    return render(request, 'menu/category.html', {'categories': categories})

@csrf_exempt  # only use this if CSRF is failing — otherwise include the CSRF token in AJAX
def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        availability = request.POST.get('availability')  # "Available" or "Unavailable"
        availability = True if availability == 'Available' else False
        image = request.FILES.get('image')

        if not (name and category_id and price):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Invalid category'}, status=400)

        item = MenuItem.objects.create(
            name=name,
            category=category,
            price=price,
            availability=availability,
            image=image
        )

        return JsonResponse({'message': 'Menu item added', 'id': item.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def edit_menu_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, id=item_id)
        
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        availability = request.POST.get('availability')
        image = request.FILES.get('image')

        # Validate inputs (basic)
        if not all([name, category_id, price, availability]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        item.name = name
        item.category = get_object_or_404(Category, id=category_id)
        item.price = price
        item.availability = True if availability == 'Available' else False

        if image:
            item.image = image  # Replace only if a new image is uploaded

        item.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



def today_special(request):
    # Sab menu items fetch kar rahe hain
    items = MenuItem.objects.all()
    today_specials = TodaySpecial.objects.all()
    return render(request, 'menu/today_special.html', {
        'items': items,
        'today_specials': today_specials
    })



@csrf_exempt
def save_today_special(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items[]')  # ['1','2'] or ['1,2']

        # Ensure we have a list of integers
        item_ids_clean = []
        for i in item_ids:
            if ',' in i:  # handle comma-separated string
                item_ids_clean.extend([int(x) for x in i.split(',') if x])
            else:
                item_ids_clean.append(int(i))

        # Create new TodaySpecial
        special = TodaySpecial.objects.create()
        special.items.set(item_ids_clean)  # assign multiple items
        special.save()

        return JsonResponse({'status':'success'})

@csrf_exempt
def save_scheduled_special(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        special_id = data.get('special_id')
        scheduled_id = data.get('scheduled_id')  # new
        start_date = data.get('start_date')
        end_date = data.get('end_date', start_date)

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        if scheduled_id:
            # Update existing ScheduledSpecial
            scheduled = ScheduledSpecial.objects.get(id=scheduled_id)
            scheduled.start_date = start_date_obj
            scheduled.end_date = end_date_obj
            scheduled.save()
            created = False
        else:
            # Create new
            scheduled, created = ScheduledSpecial.objects.update_or_create(
                special_id=special_id,
                start_date=start_date_obj,
                defaults={'end_date': end_date_obj}
            )

        return JsonResponse({
            'status': 'success',
            'scheduled_id': scheduled.id,
            'created': created
        })


from .models import ScheduledSpecial

def get_scheduled_specials(request):
    events = []
    for s in ScheduledSpecial.objects.select_related('special'):
       events.append({
    'title': s.special.name,
    'start': s.start_date.strftime("%Y-%m-%d"),
    'end': s.end_date.strftime("%Y-%m-%d") if s.end_date else None,
    'backgroundColor': "#ffc107",  # Bootstrap warning color (yellow)
    'borderColor': "#ffc107",      # same as background
    'textColor': "#000000",         # black text
})

    return JsonResponse(events, safe=False)


@csrf_exempt
def delete_scheduled_special(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        scheduled_id = data.get('scheduled_id')

        if not scheduled_id:
            return JsonResponse({'status': 'error', 'message': 'Scheduled ID missing'})

        try:
            scheduled_event = ScheduledSpecial.objects.get(id=scheduled_id)
            scheduled_event.delete()
            return JsonResponse({'status': 'success'})
        except ScheduledSpecial.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def delete_special(request, special_id):
    if request.method == 'POST':
        special = get_object_or_404(TodaySpecial, id=special_id)
        special.delete()
        return JsonResponse({'success': True, 'message': 'Special deleted successfully.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def delete_menu_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            return JsonResponse({'error': 'Category name is required'}, status=400)

        category = Category.objects.create(name=name, description=description)
        return JsonResponse({'message': 'Category added', 'id': category.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def edit_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)

        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            return JsonResponse({'error': 'Category name is required'}, status=400)

        category.name = name
        category.description = description
        category.save()

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)