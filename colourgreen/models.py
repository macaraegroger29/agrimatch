from django.db import models

class SensorData(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()

class Prediction(models.Model):
    crop_name = models.CharField(max_length=100)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField(50)
    ph = models.FloatField()
    rainfall = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.crop_name
