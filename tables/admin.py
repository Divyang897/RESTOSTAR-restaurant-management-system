from django.contrib import admin
from .models import Table, Booking


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('number',)
    list_editable = ('is_available',)  # directly admin panel me available/unavailable change kar sakte ho


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date', 'time', 'end_time','total_persons', 'contact_number', 'created_at')
    list_filter = ('date', 'time')
    search_fields = ('customer_name', 'contact_number')
    filter_horizontal = ('tables',)  # multiple tables select karne ke liye nice UI milta hai
