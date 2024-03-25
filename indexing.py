import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from collections import defaultdict

with open('autogrant.scholarships.json', 'r', encoding='utf-8') as file:
    scholarships = json.load(file)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

index = defaultdict(list)


def preprocess(text):
    if text is None:
        return []
    if isinstance(text, str):
        text = text.lower()
    else:
        text = ' '.join([str(element).lower() for element in text])
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return tokens


for scholarship in scholarships:
    scholarship_id = scholarship['_id']['$oid']
    description = scholarship.get('description', '')
    eligibility = scholarship.get('eligibility', '')

    description_tokens = preprocess(description)
    eligibility_tokens = preprocess(eligibility)

    for term in set(description_tokens + eligibility_tokens):
        index[term].append(scholarship_id)

index = dict(index)

formatted_index = [{"token": token, "documents": documents} for token, documents in index.items()]

with open('scholarship_index.json', 'w', encoding='utf-8') as file:
    json.dump(formatted_index, file, indent=2)

print("Indexing completed and saved as scholarship_index.json.")
