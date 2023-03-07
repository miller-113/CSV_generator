from django.contrib import admin
from .models import Schema, Column


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'data', 'owner', 'column_separator',
                    'column_characters')
    list_filter = ('owner',)
    search_fields = ('name', 'owner__username')
    readonly_fields = ('data',)

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    exclude = []