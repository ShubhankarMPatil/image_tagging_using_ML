import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def load_json(json_file_path):
    """Load and parse the JSON file containing image tags."""
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data

def extract_keywords(prompt):
    """Extract keywords from the user's prompt."""
    keywords = [word.lower() for word in prompt.split()]
    return keywords

def retrieve_images(json_data, keywords):
    """Retrieve and rank images based on tags."""
    matches = []

    for image_name, tags in json_data.items():
        match_count = sum(1 for keyword in keywords if keyword in tags)
        if match_count > 0:
            matches.append((image_name, tags, match_count))

    # Sort matches by match_count (best match first)
    matches = sorted(matches, key=lambda x: x[2], reverse=True)

    return matches

def display_images(image_folder, results):
    """Display matched images in a grid using Matplotlib."""
    if not results:
        print("No matching images found.")
        return
    
    num_images = len(results)
    cols = min(3, num_images)  # Limit to 3 columns per row
    rows = (num_images + cols - 1) // cols  # Calculate number of rows needed
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    axes = axes.flatten() if num_images > 1 else [axes]  # Flatten in case of multiple images

    for idx, (image_name, tags, score) in enumerate(results):
        image_path = os.path.join(image_folder, image_name)
        
        if os.path.exists(image_path):
            img = mpimg.imread(image_path)
            axes[idx].imshow(img)
            axes[idx].set_title(f"{image_name}\nTags: {', '.join(tags)}", fontsize=10)
            axes[idx].axis("off")
        else:
            print(f"Image not found: {image_path}")
    
    # Hide unused subplots
    for idx in range(len(results), len(axes)):
        axes[idx].axis("off")

    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    json_file_path = "image_data.json"  # JSON file with image tags
    image_folder = "test_images"  # Folder containing images

    json_data = load_json(json_file_path)
    user_prompt = input("Enter search prompt: ")
    keywords = extract_keywords(user_prompt)

    results = retrieve_images(json_data, keywords)
    
    display_images(image_folder, results)
