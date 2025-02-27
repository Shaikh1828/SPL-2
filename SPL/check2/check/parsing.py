import re

def extract_intents(manifest_path):
    # Regex pattern to find android intents in the format "android.intent.action.<name>"
    intent_pattern = r'android\.intent\.action\.(\w+)'

    # List to store the extracted intents
    intents = []

    # Read the manifest file and search for intents
    with open(manifest_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Search for intents in each line
            found_intents = re.findall(intent_pattern, line)
            # Add found intents to the list
            intents.extend(found_intents)

    # Remove duplicates by converting the list to a set
    unique_intents = set(intents)

    # Return the unique intents as a list
    return list(unique_intents)
import xml.etree.ElementTree as ET

def extract_permissions(manifest_file):
    # Step 1: Parse the AndroidManifest.xml file
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    # Step 2: Define the Android namespace used in the XML
    android_ns = 'http://schemas.android.com/apk/res/android'

    # Step 3: Initialize a list to hold extracted permissions
    permissions = []

    # Step 4: Find all <uses-permission> elements in the XML
    for elem in root.findall('uses-permission'):
        # Step 5: Extract the android:name attribute which contains the permission
        permission = elem.get(f'{{{android_ns}}}name')
        if permission:
            # Extract only the part after ".permission" if it exists
            if ".permission." in permission:
                clean_permission = permission.split(".permission.")[-1]
                permissions.append(clean_permission)

    return permissions