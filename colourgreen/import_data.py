import pandas as pd
from colourgreen.models import SensorData
import os
from django.db import transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'agrimatch', 'data', 'Crop_recommendation.csv')

def import_excel_to_db():
    print(f"Looking for file at: {file_path}")

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        data = pd.read_csv(file_path)
        print("Column names:", data.columns)
        print("Data types:", data.dtypes)
        print("First few rows:", data.head())

        # Check for missing values
        print("Missing values per column:", data.isnull().sum())

        sensor_data_list = []
        for _, row in data.iterrows():
            # Handle missing values
            sensor_data = SensorData(
                nitrogen=row.get('N', 0),
                phosphorus=row.get('P', 0),
                potassium=row.get('K', 0),
                temperature=row.get('temperature') if pd.notna(row.get('temperature')) else 0.0,
                humidity=row.get('humidity') if pd.notna(row.get('humidity')) else 0.0,
                ph=row.get('ph') if pd.notna(row.get('ph')) else 0.0,
                rainfall=row.get('rainfall') if pd.notna(row.get('rainfall')) else 0.0
            )
            sensor_data_list.append(sensor_data)

        # Batch insert the data for performance
        with transaction.atomic():
            SensorData.objects.bulk_create(sensor_data_list)

        print("Data imported successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

