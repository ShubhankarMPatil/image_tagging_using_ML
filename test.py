import torch
import clip
from PIL import Image

# Check if CUDA (GPU) is available; if not, use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the CLIP model and the preprocessing method
model, preprocess = clip.load("ViT-B/32", device=device)

# Load and preprocess the image
image_path = 'bird_1.jpg'  # Replace with your image path
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

# Generate image features (embeddings)
with torch.no_grad():
    image_features = model.encode_image(image)
    print("Image Embeddings Generated.")

# Example text prompts
text_inputs = clip.tokenize(["a bird sitting on a street", "a parrot with a red beak sitting on a branch", "a person dancing to music"]).to(device)

# Generate text features
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_inputs)

# Normalize the features to have unit length
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

# Compute similarity between image and text features
similarity = image_features @ text_features.T  # Matrix multiplication to get similarity

# Apply softmax to scale similarity scores between 0 and 1
similarity_scores = similarity.softmax(dim=-1)

# Print the similarity scores for each text prompt
print(similarity_scores)