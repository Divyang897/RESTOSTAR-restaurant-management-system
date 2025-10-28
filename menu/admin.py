from django.contrib import admin
from .models import Category, MenuItem,TodaySpecial,ScheduledSpecial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'availability')
    list_filter = ('category', 'availability')
    search_fields = ('name',)

@admin.register(TodaySpecial)
class TodaySpecialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_items', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    filter_horizontal = ('items',)

    def get_items(self, obj):
        # Return comma-separated list of related menu items
        return ", ".join([item.name for item in obj.items.all()])
    get_items.short_description = 'Menu Items'

@admin.register(ScheduledSpecial)
class ScheduledSpecialAdmin(admin.ModelAdmin):
    list_display = ('special', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'special')
    search_fields = ('special__name',)
    ordering = ('-start_date',)