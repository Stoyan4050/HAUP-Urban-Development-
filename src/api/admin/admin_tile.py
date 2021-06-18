"""
admin_tile.py
"""

from django.contrib import admin
from api.models.tile import Tile


@admin.register(Tile)
class AdminTile(admin.ModelAdmin):
    """
    @admin.register(Tile)
    class AdminTile(admin.ModelAdmin)
    """

    model = Tile
