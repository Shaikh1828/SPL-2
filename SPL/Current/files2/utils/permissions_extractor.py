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

# import xml.etree.ElementTree as ET

# def extract_permissions(manifest_file):
#     # Step 1: Parse the AndroidManifest.xml file
#     tree = ET.parse(manifest_file)
#     root = tree.getroot()

#     # Step 2: Define the Android namespace used in the XML
#     android_ns = 'http://schemas.android.com/apk/res/android'

#     # Step 3: Initialize a list to hold extracted permissions
#     permissions = []

#     # Step 4: Find all <uses-permission> elements in the XML
#     for elem in root.findall('uses-permission'):
#         # Step 5: Extract the android:name attribute which contains the permission
#         permission = elem.get(f'{{{android_ns}}}name')
#         if permission:
#             # Remove "android.permission." prefix if it exists
#             clean_permission = permission.replace("android.permission.", "")
#             permissions.append(clean_permission)  # Step 6: Add to the list of permissions

#     return permissions

# # Example usage
# manifest_file = 'AndroidManifest.xml'
# permissions_list = extract_permissions(manifest_file)

# # Step 7: Print all permissions extracted from the manifest file
# print("App Permissions:")
# for permission in permissions_list:
#     print(permission)
