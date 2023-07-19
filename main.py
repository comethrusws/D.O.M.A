import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PyPDF2 import PdfReader
import glob
from langdetect import detect
from googletrans import Translator
from googlesearch import search
import time

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# predefined patterns and responses
patterns = [
    (["hello", "hi", "hey"], ["Hi!", "Hello!", "Hey!"]),
    (["how", "are", "you"], ["I'm good, thanks!", "I'm doing great!", "I'm fine."]),
    (["name"], ["I'm a chatbot. My Name is DOMA!", "You can call me DOMA!", "I don't have a name."]),
    (["what","is","your","name"], ["I'm a chatbot. My Name is DOMA!", "You can call me DOMA!", "I don't have a name."]),
    (["bye", "goodbye"], ["Goodbye!", "See you later!", "Take care!"]),
    (["how", "old", "you"], ["I am just a computer program, so I don't have an age."]),
    (["what", "your", "purpose"], ["I am here to assist and answer your questions."]),
    (["who", "created", "you"], ["I was created by a Developer named Basab."]),
    (["tell", "joke"], ["Why don't scientists trust atoms? Because they make up everything!"]),
]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# user input preprocessing
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return filtered_tokens


def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error while extracting text from PDF: {str(e)}")
        return ''

# load and preprocess pdf
def load_pdfs():
    pdf_files = glob.glob("C:/Users/Basab/Desktop/D.O.M.A/Database/*.pdf")
    pdf_texts = []  # Initialize the list to store text from PDFs
    for pdf_file in pdf_files:
        file_path = pdf_file
        text = extract_text_from_pdf(pdf_file)
        pdf_texts.append(text)
    return pdf_texts

def generate_response(user_input, pdf_texts):
    preprocessed_input = preprocess_input(user_input)
    for pattern, responses in patterns:
        if all(word in preprocessed_input for word in pattern):
            return random.choice(responses)

    combined_text = ' '.join(pdf_texts)

    detected_lang = detect(user_input)

    if detected_lang != 'en':
        translator = Translator()
        try:
            user_input = translator.translate(user_input, src=detected_lang, dest='en').text
        except (AttributeError, ConnectionError) as e:
            print(f"Google Translate API error: {e}")
            return "Oops! Something went wrong with translation. Please try again later."
        time.sleep(1)

    # Web search
    search_results = list(search(user_input, num=3, stop=3))
    if search_results:
        return f"Here are some search results for '{user_input}':\n" + "\n".join(search_results)

    return "DOMA: I'm sorry, I don't understand that. Can you please rephrase?"

pdf_texts = load_pdfs()

def main():
    pdf_texts = load_pdfs()  # Load and preprocess the pdfs
    while True:
        user_input = input("User: ")
        response = generate_response(user_input, pdf_texts)
        if not response:
            # Basic conversation responses
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

# Main loop
while True:
    user_input = input("User: ")
    response = generate_response(user_input, pdf_texts)
    if not response:
        # Basic conversation responses
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