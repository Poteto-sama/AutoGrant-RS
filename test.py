import json

# Load scholarship index data
with open('scholarship_index.json', 'r', encoding='utf-8') as file:
    scholarship_index = json.load(file)

# Extract tokens from each dictionary in the index
tokens = [entry['token'] for entry in scholarship_index]

# Print the tokens
print("Tokens:")
for token in tokens:
    print(token)
