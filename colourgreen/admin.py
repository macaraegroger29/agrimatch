from django.contrib import admin
from .models import SensorData

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall')  # Add fields you want to display
    list_filter = ()
    
admin.site.register(SensorData, SensorDataAdmin)
