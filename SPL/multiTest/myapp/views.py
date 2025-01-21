# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UploadedFile
from .forms import UploadFileForm
import os
from django.conf import settings
# myapp/views.py
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# def services(request):
#     return render(request, 'services.html')


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'apk'}

# Function to check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# @csrf_exempt
def index(request):
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.FILES:
            messages.error(request, 'No file part')
            return redirect('index')

        file = request.FILES['file']

        # If user does not select a file
        if file.name == '':
            messages.error(request, 'No selected file')
            return redirect('index')

        # If file has a valid extension
        if allowed_file(file.name):
            try:
                # Save the file to the media/uploads directory
                filename = file.name
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                
                with open(filepath, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Save file information to the database
                new_file = UploadedFile(filename=filename, filepath=filepath)
                new_file.save()

        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     uploaded_file = form.save()  # Save to database

        #     # Process the file after saving
        #     file_path = uploaded_file.file.path

        #     messages.success(request, f'File successfully uploaded: ')
        #     return redirect('index')
            except Exception as e:
                messages.error(request, f'Error saving file: {e}')
        else:
            messages.error(request, 'Invalid file type')
            return redirect('index')

    return render(request, 'index.html')
