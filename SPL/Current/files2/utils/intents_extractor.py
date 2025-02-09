# import re

# def extract_intents(manifest_path):
#     # Regex pattern to find android intents in the format "android.intent.action"
#     intent_pattern = r'android\.intent\.action\.\w+'

#     # List to store the extracted intents
#     intents = []

#     # Read the manifest file and search for intents
#     with open(manifest_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             # Search for intents in each line
#             found_intents = re.findall(intent_pattern, line)
#             # Add found intents to the list
#             intents.extend(found_intents)

#     # Remove duplicates by converting the list to a set
#     unique_intents = set(intents)

#     # Return the unique intents as a list
#     return list(unique_intents)
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
