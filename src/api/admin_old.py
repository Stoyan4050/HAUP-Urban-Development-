"""
admin_old.py
"""

from django.contrib import admin
from .models import Tile, Classification


@admin.register(Tile)
class TileAdmin(admin.ModelAdmin):
    """
    @admin.register(Tile)
    class TileAdmin(admin.ModelAdmin)
    """

    model = Tile


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    """
    @admin.register(Classification)
    class ClassificationAdmin(admin.ModelAdmin)
    """

    model = Classification
