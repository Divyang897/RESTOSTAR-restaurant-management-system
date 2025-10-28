from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import Table, Booking
from datetime import datetime
import json

from django.http import JsonResponse
from datetime import datetime, date
from .models import Booking

def today_bookings(request):
    """
    Return all booked tables for today with customer info.
    """
    today = date.today()
    bookings = Booking.objects.filter(date=today)
    booked_tables = []

    for booking in bookings:
        for table in booking.tables.all():
            booked_tables.append({
                'table_number': table.number,
                'customer_name': booking.customer_name, 
                'total_persons': booking.total_persons,
                'contact_number': booking.contact_number,
                'start_time': booking.time.strftime('%H:%M'),
                'end_time': booking.end_time.strftime('%H:%M'),
            })
    
    return JsonResponse({'booked_tables': booked_tables})


@login_required(login_url='/login/')
def table_home(request):
    tables = Table.objects.all().order_by('number')
    bookings = Booking.objects.all()  # lowercase for clarity

    for t in tables:
        t.chair_range = range(min(t.capacity, 10))

    return render(request, 'tables/index.html', {'tables': tables, 'bookings': bookings})



def table_booking_page(request):
    tables = Table.objects.all().order_by('number')
    return render(request, 'booking/table_booking.html', {'tables': tables})

def check_availability(request):
    """
    Check booked tables for selected date & time with customer info for tooltip.
    """
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')

    if not date_str or not time_str:
        return JsonResponse({'error': 'Invalid date or time'}, status=400)

    # Convert to Python date/time
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    time_obj = datetime.strptime(time_str, '%H:%M').time()

    # All bookings for that date
    bookings = Booking.objects.filter(date=date_obj)
    booked_tables = []

    for booking in bookings:
        # अगर चुना गया time उस booking के अंदर आता है
        if booking.time <= time_obj <= booking.end_time:
            for table in booking.tables.all():
                booked_tables.append({
                    'table_number': table.number,
                    'customer_name': booking.customer_name,
                    'total_persons': booking.total_persons,
                    'contact_number': booking.contact_number,
                    'start_time': booking.time.strftime('%H:%M'),
                    'end_time': booking.end_time.strftime('%H:%M'),
                })

    return JsonResponse({'booked_tables': booked_tables})


def submit_booking(request):
    """
    Save booking data coming from JS (AJAX POST).
    """
    if request.method == 'POST':
        data = json.loads(request.body)

        date_str = data.get('date')
        time_str = data.get('time')
        name = data.get('customer_name')
        total_persons = data.get('total_persons')
        contact = data.get('contact_number')
        table_numbers = data.get('tables', [])

        if not all([date_str, time_str, name, contact, table_numbers]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        booking = Booking.objects.create(
            date=date_obj,
            time=time_obj,
            customer_name=name,
            total_persons=total_persons,
            contact_number=contact
        )

        # Add selected tables
        tables = Table.objects.filter(number__in=table_numbers)
        booking.tables.set(tables)

        # Mark tables unavailable
        for t in tables:
            t.is_available = False
            t.save()

        return JsonResponse({'success': True, 'message': 'Booking successful!'})

    return JsonResponse({'error': 'Invalid request'}, status=405)


def tabless(request):
    # Get all tables ordered by number
    tables = Table.objects.all().order_by('number')

    # Optionally, add chair_range for rendering chairs in template
    for t in tables:
        t.chair_range = range(t.capacity)  # or min(t.capacity, 10) if you want max 10 chairs

    return render(request, 'tables/tabless.html', {'tables': tables})


def add_tables(request):
    if request.method == 'POST':
        # Extract data from POST request
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')

        if not number or not capacity:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        # Create and save new table
        table = Table.objects.create(
            number=number,
            capacity=capacity,
            is_available=True
        )
        table.save()

        return JsonResponse({'success': True, 'message': 'Table added successfully!'})

    return render(request, 'tables/tabless.html')


def edit_table(request, id):
    if request.method == 'POST':
        # Extract data from POST request
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')
        is_available = request.POST.get('is_available') == 'Available'

        if not number or not capacity:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        try:
            table = Table.objects.get(id=id)
            table.number = number
            table.capacity = capacity
            table.is_available = is_available
            table.save()
            return JsonResponse({'success': True, 'message': 'Table updated successfully!'})
        except Table.DoesNotExist:
            return JsonResponse({'error': 'Table not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=405)