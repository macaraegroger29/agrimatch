# Generated by Django 5.1 on 2024-08-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colourgreen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
