from django.shortcuts import render
from .forms import SensorDataForm
from .models import Prediction
import joblib
from django.db.models import Count
import json

model = joblib.load('C:/Users/jao/projects/agrimatch/colourgreen/models/RandomForest.pkl')

def index(request):
    prediction = None
    if request.method == 'POST':
        form = SensorDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            features = [[data['nitrogen'], data['phosphorus'], data['potassium'],
                         data['temperature'], data['humidity'], data['ph']]]
            crop_prediction = model.predict(features)[0]

            # Save the prediction to the database
            Prediction.objects.create(
                crop_name=crop_prediction,
                nitrogen=data['nitrogen'],
                phosphorus=data['phosphorus'],
                potassium=data['potassium'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                ph=data['ph'],
                rainfall=data['rainfall']
            )

            prediction = crop_prediction
    else:
        form = SensorDataForm()

    recent_predictions = Prediction.objects.order_by('-date')[:5]

    return render(request, 'index.html', {'form': form, 'prediction': prediction, 'recent_predictions': recent_predictions})

def examples(request):
    # Get the most recent prediction (this is the predicted crop from index.html)
    last_prediction = Prediction.objects.latest('date')
    predicted_crop = last_prediction.crop_name

    # Query to get the top 4 crops (excluding the predicted crop)
    top_crops = (Prediction.objects
                 .exclude(crop_name=predicted_crop)
                 .values('crop_name')
                 .annotate(total=Count('crop_name'))
                 .order_by('-total')[:4])  # Get the next 4 crops

    # Prepare data for the chart
    crop_names = [crop['crop_name'] for crop in top_crops]
    crop_counts = [crop['total'] for crop in top_crops]

    # Add the predicted crop as the first entry with a custom highest count
    predicted_crop_count = max(crop_counts) + 1 if crop_counts else 1  # Make sure it's the highest
    crop_names.insert(0, predicted_crop)  # Insert predicted crop at the top
    crop_counts.insert(0, predicted_crop_count)  # Insert the highest count for the predicted crop

    # Convert lists to JSON strings for use in JavaScript
    crop_names_json = json.dumps(crop_names)
    crop_counts_json = json.dumps(crop_counts)

    context = {
        'crop_names_json': crop_names_json,
        'crop_counts_json': crop_counts_json,
        'predicted_crop': predicted_crop
    }
    return render(request, 'examples.html', context)


def another_page(request):
    return render(request, 'another_page.html')

def contact(request):
    return render(request, 'contact.html')

def page(request):
    return render(request, 'page.html')

def predict_crop(request):
    if request.method == 'POST':
        form = SensorDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            features = [[data['nitrogen'], data['phosphorus'], data['potassium'],
                         data['temperature'], data['humidity'], data['ph']]]
            
            # Predict crop
            crop_prediction = model.predict(features)[0]

            # Save the prediction in the database
            Prediction.objects.create(
                crop_name=crop_prediction,
                nitrogen=data['nitrogen'],
                phosphorus=data['phosphorus'],
                potassium=data['potassium'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                ph=data['ph'],
                rainfall=data['rainfall']
            )

            # Store predicted crop in session
            request.session['predicted_crop'] = crop_prediction

            # Continue rendering index.html without redirection
            recent_predictions = Prediction.objects.order_by('-date')[:5]
            return render(request, 'index.html', {'prediction': crop_prediction, 'recent_predictions': recent_predictions})
    
    return redirect('index')

    