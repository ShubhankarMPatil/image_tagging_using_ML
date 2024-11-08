from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os

# Initialize device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load BLIP model for dynamic image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def resize_image(image, max_size=(512, 512)):
    """Resize image to reduce processing time, keeping aspect ratio."""
    image.thumbnail(max_size)
    return image

def generate_caption(image_path):
    """Generates caption for a given image."""
    image = Image.open(image_path)
    resized_image = resize_image(image)  # Resize for efficiency
    inputs = processor(images=resized_image, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=50, min_length=10, num_beams=10)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
