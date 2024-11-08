import spacy

# Load SpaCy English model for dependency parsing
nlp = spacy.load("en_core_web_sm")

def extract_noun_adj_pairs(caption):
    """Extracts noun-adjective pairs from a caption."""
    doc = nlp(caption)
    noun_adj_pairs = []

    for token in doc:
        if token.pos_ == "NOUN":
            adjectives = [child.text for child in token.children if child.pos_ == "ADJ"]
            if adjectives:
                for adj in adjectives:
                    noun_adj_pairs.append(f"{adj} {token.text}")
            else:
                noun_adj_pairs.append(token.text)

    return list(set(noun_adj_pairs))  # Remove duplicates
