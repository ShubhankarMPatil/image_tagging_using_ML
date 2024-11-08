import spacy

# Load the SpaCy model with NER capability
nlp = spacy.load('en_core_web_lg')

# Example sentence
sentence = "A couple standing in a forest looking at the sky."

# Process the sentence
doc = nlp(sentence)

# Extract locations using NER
locations = []
for ent in doc.ents:
    if ent.label_ == 'LOC':  # GPE (Geopolitical Entity), LOC (Other Locations)
        locations.append(ent.text)

print(doc.ents)
print("Locations:", locations)
