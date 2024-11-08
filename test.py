from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from anytree import Node, RenderTree
import os
import spacy
import torch

# use GPU for computation if CUDA is available else use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

# Load BLIP model for dynamic image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model = model.to(device)

# load the SpaCy English language model for parsing dependencies
nlp = spacy.load("en_core_web_sm")

# Example image path
image_path = "Screenshot (39).png"
image = Image.open(image_path)

# Generate dynamic description for the image
inputs = processor(images=image, return_tensors="pt").to(device)
output = model.generate(**inputs, max_length = 50, min_length = 10, num_beams = 10)
caption = processor.decode(output[0], skip_special_tokens=True)

doc = nlp(caption)

noun_adj_pairs = []

for token in doc:
    if token.pos_ == "NOUN":
        adjectives = [child.text for child in token.children if child.pos_ == "ADJ"]
        if adjectives:
            for adj in adjectives:
                noun_adj_pairs.append(f"{adj} {token.text}")
        elif token.pos_ == "NOUN":
            noun_adj_pairs.append(token.text)

print("Generated Caption: ", caption)
print("Adjective-Noun pairs", list(set(noun_adj_pairs)))