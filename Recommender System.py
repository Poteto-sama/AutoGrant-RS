import json
from Levenshtein import distance
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re


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


with open('scholarship_index.json', 'r', encoding='utf-8') as file:
    scholarship_index = json.load(file)

with open('autogrant.userdata.single.json', 'r', encoding='utf-8') as file:
    user_data_list = json.load(file)

with open('technical_terms.json', 'r', encoding='utf-8') as file:
    document_terms = json.load(file)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

degree_weight = 1.2
stream_weight = 0.8
country_weight = 1.3
bio_weight = 0.1
document_terms_weight = 0.08

for user_data in user_data_list:
    user_bio = user_data.get('user_bio', '')
    user_degree = user_data.get('degree_choice', '')
    user_stream = user_data.get('stream_choice', '')
    user_country = user_data.get('country_choice', '')

    user_degree_tokens = user_degree.lower().split()
    user_stream_tokens = user_stream.lower().split()
    user_country_tokens = user_country.lower().split()
    user_bio_tokens = preprocess(user_bio)
    scholarship_scores = {}

    for token_data in scholarship_index:
        token = token_data['token']
        documents = token_data['documents']

        relevance_score = 0
        for user_param_tokens, weight in [(set(user_degree_tokens), degree_weight),
                                          (set(user_stream_tokens), stream_weight),
                                          (set(user_country_tokens), country_weight),
                                          (set(user_bio_tokens), bio_weight),
                                          (set(document_terms), document_terms_weight)]:
            for user_token in user_param_tokens:
                similarity_score = 1 - (distance(token, user_token) / max(len(token), len(user_token)))
                if similarity_score > 0.75:
                    relevance_score += similarity_score * weight

        for scholarship_id in documents:
            scholarship_scores[scholarship_id] = scholarship_scores.get(scholarship_id, 0) + relevance_score

    sorted_scholarships = sorted(scholarship_scores.items(), key=lambda x: x[1], reverse=True)

    print("Recommended Scholarships for User:")
    for scholarship_id, relevance_score in sorted_scholarships:
        print("- Scholarship:", scholarship_id, "| Relevance Score:", relevance_score)
    recommendations = sorted_scholarships[:5]
    top_5 = []
    for scholarship_id, relevance_score in recommendations:
        top_5.append({
            "id": scholarship_id,
            "relevance": relevance_score
        })
    with open('top_5.json', 'w', encoding='utf-8') as file:
        json.dump(top_5, file, indent=2)
