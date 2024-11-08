import os
from image_captioner import generate_caption
from tag_extractor import extract_noun_adj_pairs
from tag_storage import store_image_tags

def process_images_from_directory(directory_path):
    """Process all images in a given directory and store their tags."""
    # Supported image file extensions
    supported_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    # List all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file has a supported image extension
        if os.path.splitext(filename)[1].lower() in supported_extensions:
            image_path = os.path.join(directory_path, filename)
            print(f"Processing image: {filename}")

            # Generate caption for the image
            caption = generate_caption(image_path)
            print("Generated Caption:", caption)

            # Extract noun-adjective pairs (tags) from the caption
            tags = extract_noun_adj_pairs(caption)
            print("Tags:", tags)

            # Store the image name and tags in JSON file
            store_image_tags(filename, tags)
            print(f"Data saved for image '{filename}'\n")

# Specify the directory containing images
directory_path = "test_images"  # Replace with your directory path

# Process all images in the specified directory
process_images_from_directory(directory_path)
