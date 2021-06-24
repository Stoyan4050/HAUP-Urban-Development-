"""
admin_classification.py
"""
from django.contrib import admin
from api.models.classification import Classification


@admin.register(Classification)
class AdminClassification(admin.ModelAdmin):
    """
    @admin.register(Classification)
    class AdminClassification(admin.ModelAdmin)
    """

    model = Classification
