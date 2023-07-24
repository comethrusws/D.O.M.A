#D.O.M.A : Deep-learning Oriented Multilingual Assistant

import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langdetect import detect
from googletrans import Translator
import time
import googlesearch
import threading
import transformers
import tensorflow as tf

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

t5_model = transformers.TFT5ForConditionalGeneration.from_pretrained('t5-small')
t5_tokenizer = transformers.T5Tokenizer.from_pretrained('t5-small')

#patterns ra responses(predefined)
patterns = [
    (["hello", "hi", "hey"], ["Hi there!", "Hello!", "Hey! What is up?"]),
    (["how", "are", "you"], ["I'm good, thanks!", "I'm doing great!", "I'm fine.How are you?"]),
    (["name"], ["I am DOMA. Nice to meet you!", "You can call me DOMA!"]),
    (["what", "is", "your", "name"], ["My Name is DOMA! I'm a chatbot. ", "You can call me DOMA!","Hi! I a DOMA!"]),
    (["bye", "goodbye"], ["Goodbye!", "See you later!", "Take care!"]),
    (["how", "old", "you"], ["I am just a computer program, so I don't have an age."]),
    (["what", "your", "you","do","can","ability","purpose"], ["I am here to assist and answer your questions."]),
    (["who", "created", "made", "you"], ["I was created by a Developer named Basab."]),
    (["tell", "me", "jokes" ,"joke"], ["Why don't scientists trust atoms? Because they make up everything!⚛","Why was 6 aftrai of 7? Because 7,8,9!😂" "What do you call a south asian electrician? A-Shok(Get it?)🤯⚡","what happens to a ilegally parked frog? It gets Toad away.🐸"]),
]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# user input preprocess
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return filtered_tokens

def generate_response(user_input):
    # Preprocess the user input
    preprocessed_input = preprocess_input(user_input)
    for pattern, responses in patterns:
        if any(word in preprocessed_input for word in pattern):
            return random.choice(responses)

    detected_lang = detect(user_input)

    if detected_lang != 'en':
        translator = Translator()
        try:
            translated_text = translator.translate(user_input, src=detected_lang, dest='en')
            user_input = translated_text.text
        except Exception as e:
            print(f"Translation error: {e}")
            return "Oops! Something went wrong with translation. Can you repeat that?"
        time.sleep(1)

    if "search" in preprocessed_input:
        search_query = user_input.replace("search", "").strip()
        try:
            # google search perform garney
            search_results = googlesearch.search(search_query, num_results=3)
            if search_results:
                return "\n".join(search_results)
            else:
                return "Sorry, I couldn't find any relevant results for your search."
        except Exception as e:
            print(f"Google search error: {e}")
            return "Oops! Something went wrong with the search. Please try again later."

    # If no predefined patterns match and not a search query, T5 model for response generation
    inputs = t5_tokenizer("DOMA: " + user_input, return_tensors="tf", max_length=512, padding="max_length", truncation=True)
    outputs = t5_model.generate(inputs.input_ids, max_length=100, num_return_sequences=1, early_stopping=True)
    response = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

def main():
    while True:
        user_input = input("User: ")
        response = generate_response(user_input)
        if not response:
            # Basic conversation response haru
            if "thank you" in user_input.lower():
                print("DOMA: You're welcome!")
            elif "how are you" in user_input.lower():
                print("DOMA: I'm doing well, thank you!")
            elif "hello" in user_input.lower():
                print("DOMA: Hi! How are you doing today?")
            else:
                print("DOMA: I'm sorry, I don't understand that. Can you please rephrase?")
        else:
            print("DOMA:", response)

if __name__ == "__main__":
    main()
