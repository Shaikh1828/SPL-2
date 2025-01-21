import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
from .utils.permissions_extractor import extract_permissions
from .utils.intents_extractor import extract_intents

# def process_file(file_path):
#     df = pd.read_csv(file_path)
#     summary = f'Total rows: {df.shape[0]}, Total columns: {df.shape[1]}'
#     return summary

import subprocess
import shutil
import tempfile
import uuid

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')



def extract_manifest(apk_path, output_dir):
    apktool_jar = "C:\\apktool\\apktool_2.10.0.jar"  # Path to apktool.jar
    # temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    
    # # print(f"Temporary directory created at: {temp_dir}")
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    temp_dir = os.path.join(output_dir, uuid.uuid4().hex)
    os.makedirs(temp_dir, exist_ok=True)  
    try:
               
        # Command to run Apktool

        command = [
            "java", "-Xmx4G","-jar", apktool_jar, "d", apk_path, "-o", temp_dir,"--no-src", "-f"
        ]

        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        

        if result.returncode == 0:
            # Path to the AndroidManifest.xml
            manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")

            
            if os.path.exists(manifest_path):
                delete_all_except(manifest_path)
                return manifest_path
            # return manifest_path
            # #     # Read the manifest content
            #     with open(manifest_path, 'r', encoding='utf-8') as f:
            #         manifest_content = f.read()
            # #with open(manifest_path, 'r', encoding='utf-8', errors='replace') as f:
            # #         manifest_content = f.read()
            #     return manifest_content  # Return manifest content
            else:
                shutil.rmtree(temp_dir)
                return "Manifest file not found in APK."

        else:
            #shutil.rmtree(temp_dir)
            return f"Error: {result.stderr}"

    except Exception as e:
        #shutil.rmtree(temp_dir)
        return f"An error occurred: {e}"


def delete_all_except(file_to_keep):
    """Delete all files and folders except the specified file."""
    parent_dir = os.path.dirname(file_to_keep)

    # Traverse the directory and delete everything except the target file
    for root, dirs, files in os.walk(parent_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != file_to_keep:
                os.remove(file_path)  # Delete other files

        for directory in dirs:
            dir_path = os.path.join(root, directory)
            shutil.rmtree(dir_path)  


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save to database

            # Process the file after saving
            file_path = uploaded_file.file.path
            # return file_path
            # result = process_file(file_path)  # Call your tool here
            # result = extract_manifest(file_path,"E:\\5th Sem\\SPL-2\\SPL-2\\SPL\\multiTest\\Newmedia\\temp")
            manifestpath = extract_manifest(file_path,"E:\\5th Sem\\SPL-2\\SPL-2\\SPL\\multiTest\\Newmedia\\temp")
            permissions = extract_permissions(manifestpath)
            intents = extract_intents(manifestpath)

            # Display the extracted features
            return render(request, 'result.html', {
                # 'manifest_content': result,
                'permissions': permissions,
                'intents': intents
            })
            # # Display the result to the user
            # return render(request, 'result.html', {'result': result})

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

