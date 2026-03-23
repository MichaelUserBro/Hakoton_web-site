from django.contrib import admin
from .models import PointHistory

@admin.register(PointHistory)
class PointHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'created_at')
    readonly_fields = ('created_at',) # Историю нельзя менять вручную