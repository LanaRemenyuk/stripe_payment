from django.contrib import admin

from .models import Discount, Item, Order, Tax

EMPTY_VALUE = '-пусто-'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Представляет модель Item в интерфейсе администратора."""
    list_display = ('id', 'name', 'description', 'price')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE
