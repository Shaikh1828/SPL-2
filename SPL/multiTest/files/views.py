import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

# Simulate file processing (customize this to your needs)
# def process_file(file_path):
#     # Example: Count number of lines in a text file
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#     return f'Total lines: {len(lines)}'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save to database

            # Process the file after saving
            file_path = uploaded_file.file.path
            # result = process_file(file_path)  # Call your tool here

            # Display the result to the user
            return redirect('index')

    else:
        form = UploadFileForm()

    return render(request, 'home.html', {'form': form})

import pandas as pd

def process_file(file_path):
    df = pd.read_csv(file_path)
    summary = f'Total rows: {df.shape[0]}, Total columns: {df.shape[1]}'
    return summary
