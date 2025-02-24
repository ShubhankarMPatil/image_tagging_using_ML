import json

def load_json(json_file_path):
    """Load and parse the JSON file containing image tags."""
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data

def extract_keywords(prompt):
    """Extract keywords from the user's prompt."""
    # Simplistic approach: Split into words and normalize
    keywords = [word.lower() for word in prompt.split()]
    return keywords

def retrieve_images(json_data, keywords):
    """Retrieve and rank images based on tags."""
    matches = []

    for image_name, tags in json_data.items():
        # Count how many keywords match the tags
        match_count = sum(1 for keyword in keywords if keyword in tags)
        if match_count > 0:
            matches.append((image_name, tags, match_count))

    # Sort matches by match_count (best match first)
    matches = sorted(matches, key=lambda x: x[2], reverse=True)

    return matches

# Example usage
if __name__ == "__main__":
    json_file_path = "image_data.json"  # Replace with your JSON file path
    json_data = load_json(json_file_path)

    user_prompt = input()
    keywords = extract_keywords(user_prompt)

    results = retrieve_images(json_data, keywords)

    if results:
        print("Matching Images:")
        for image, tags, score in results:
            print(f"Image: {image}, Tags: {', '.join(tags)}, Score: {score}")
    else:
        print("No matching images found.")
