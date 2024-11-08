import json
import os

def load_data(file_path="image_data.json"):
    """Load existing data from JSON or create a new file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_data(data, file_path="image_data.json"):
    """Save data to JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def store_image_tags(image_name, tags, file_path="image_data.json"):
    """Store image name and tags to a JSON file."""
    data = load_data(file_path)
    data[image_name] = tags
    save_data(data, file_path)
