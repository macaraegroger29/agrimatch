from django import forms
from .models import SensorData
from .forms import PredictionForm 


class SensorDataForm(forms.ModelForm):
    class Meta:
        model = SensorData
        fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
