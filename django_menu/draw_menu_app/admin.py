from django.contrib import admin
from draw_menu_app.models import Menu, Item


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'parent')
    list_filter = ('menu', 'parent')

