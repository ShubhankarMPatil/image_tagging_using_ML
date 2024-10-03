from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from anytree import Node, RenderTree
import os
import spacy

# Load BLIP model for dynamic image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# load the SpaCy English language model for parsing dependencies
nlp = spacy.load("en_core_web_sm")

# Example image path
image_path = "testImage.jpeg"
image = Image.open(image_path)

# Generate dynamic description for the image
inputs = processor(images=image, return_tensors="pt")
output = model.generate(**inputs, max_length = 50, min_length = 30, num_beams = 5)
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
print("Adjective-Noun pairs", noun_adj_pairs)

# Split the generated description into potential tags
tags = caption.split()

# Dynamically create a hierarchy based on general-to-specific logic
root = Node("root")

# Assuming the first tags are more generic, refine as needed
for i, tag in enumerate(tags):
    if i == 0:
        # Generic tag at the top
        child = Node(tag, parent=root)
    else:
        # More specific tags as we go down
        Node(tag, parent=child)

# Display the dynamically generated tree
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")
