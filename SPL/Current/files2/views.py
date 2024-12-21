import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
from .utils.permissions_extractor import extract_permissions
from .utils.intents_extractor import extract_intents
from .utils.update_database import update_database

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
    #temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    

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
            manifestpath = extract_manifest(file_path,"E:\\5th Sem\\SPL-2\\SPL-2\\SPL\\Current\\New")
            permissions = extract_permissions(manifestpath)
            intents = extract_intents(manifestpath)
            features=[]
            features= permissions+intents
            update_database(uploaded_file.file.name, features)
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




def check_device(request):
    """Check if any device is connected."""
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]
        return JsonResponse({"success": True, "devices": devices})
    except subprocess.CalledProcessError as e:
        return JsonResponse({"success": False, "error": e.stderr})


def list_packages(request):
    """List all installed packages on the connected device."""
    try:
        result = subprocess.run(["adb", "shell", "pm", "list", "packages","-3"], capture_output=True, text=True, check=True)
        packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]
        return JsonResponse({"success": True, "packages": packages})
    except subprocess.CalledProcessError as e:
        return JsonResponse({"success": False, "error": e.stderr})

# import subprocess

# def extract_apk(request):
#     package_name = request.GET.get("package_name")
#     output_dir = "./extracted_apks/"
#     os.makedirs(output_dir, exist_ok=True)

#     try:
#         # Get the actual APK path
#         command = ["adb", "shell", "pm", "path", package_name]
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         apk_path = result.stdout.strip().split(":")[-1]

#         # Pull the APK file from the device
#         pull_command = ["adb", "pull", apk_path, output_dir]
#         pull_result = subprocess.run(pull_command, capture_output=True, text=True, check=True)

#         return JsonResponse({"success": True, "message": "APK extracted successfully."})
#     except subprocess.CalledProcessError as e:
#         return JsonResponse({"success": False, "error": e.stderr})


from django.http import JsonResponse
from django.shortcuts import render

# def result_view(request):
#     permissions = request.GET.get("permissions", "").split(",")
#     intents = request.GET.get("intents", "").split(",")
#     return render(request, "result.html", {
#         "permissions": permissions,
#         "intents": intents
#     })



def extract_apk(request):
    """Extract the APK of a specified package and analyze its contents."""
    package_name = request.GET.get("package_name")
    if not package_name:
        return JsonResponse({"success": False, "error": "Package name is required."})

    try:
        # Run the adb command to get APK paths
        result = subprocess.run(
            ["adb", "shell", "pm", "path", package_name],
            capture_output=True, text=True, check=True
        )

        # Split the result into lines and process each line
        apk_paths = result.stdout.splitlines()
        base_apk_path = None

        for apk_path in apk_paths:
            if apk_path.endswith("base.apk"):
                base_apk_path = apk_path
                break  # Stop after finding the first APK path (you can customize this logic)

        if not base_apk_path:
            return JsonResponse({"success": False, "error": "Base APK not found."})

        base_apk_path = base_apk_path.strip().split(":")[-1]
        local_base_apk_path = f"./extracted_apks/{package_name}-base.apk"

        # Pull the base APK to the local machine
        subprocess.run(
            ["adb", "pull", base_apk_path, local_base_apk_path],
            check=True
        )

        # Ensure the APK was pulled correctly
        if not os.path.exists(local_base_apk_path):
            return JsonResponse({"success": False, "error": "Failed to pull base APK."})
        
        manifest_path = extract_manifest(local_base_apk_path, "E:\\5th Sem\\SPL-2\\SPL-2\\SPL\\Current\\New")
        permissions = extract_permissions(manifest_path)
        intents = extract_intents(manifest_path)
        print("Permissions-",permissions)
        print()
        print("Intents",intents)
        # Return analysis results to the user
        return render(request, 'result.html', {
            'permissions': permissions,
            'intents': intents
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# def extract_apk(request):
#     """Extract the APK of a specified package and analyze its contents."""
#     package_name = request.GET.get("package_name")
#     if not package_name:
#         return JsonResponse({"success": False, "error": "Package name is required."})

#     try:
#         # Run the adb command to get APK paths
#         result = subprocess.run(
#             ["adb", "shell", "pm", "path", package_name],
#             capture_output=True, text=True, check=True
#         )

#         # Split the result into lines and process each line
#         apk_paths = result.stdout.splitlines()
#         base_apk_path = None

#         for apk_path in apk_paths:
#             if apk_path.endswith("base.apk"):
#                 base_apk_path = apk_path
#                 break  # Stop after finding the first APK path (you can customize this logic)

#         if not base_apk_path:
#             return JsonResponse({"success": False, "error": "Base APK not found."})

#         base_apk_path = base_apk_path.strip().split(":")[-1]
#         # Pull the base APK to the local machine
#         local_base_apk_path = f"./extracted_apks/{package_name}-base.apk"
#         subprocess.run(
#             ["adb", "pull", base_apk_path, local_base_apk_path],
#             check=True
#         )
#         if base_apk_path:
#             manifest_path = extract_manifest(local_base_apk_path, "E:\\5th Sem\\SPL-2\\SPL-2\\SPL\\Current\\New")
#             permissions = extract_permissions(manifest_path)
#             intents = extract_intents(manifest_path)

#             # Return analysis results to the user
#             return render(request, 'result.html', {
#                 'permissions': permissions,
#                 'intents': intents
#             })

#         return JsonResponse({"success": False, "error": "No APKs to analyze."})

#     except subprocess.CalledProcessError as e:
#         return JsonResponse({"success": False, "error": e.stderr})
