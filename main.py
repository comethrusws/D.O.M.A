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

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

#predefined patterns and resppnses
patterns = [
    (["hello", "hi", "hey"], ["Hi!", "Hello!", "Hey!"]),
    (["how", "are", "you"], ["I'm good, thanks!", "I'm doing great!", "I'm fine."]),
    (["name"], ["I'm a chatbot.", "You can call me DOMA!", "I don't have a name."]),
    (["bye", "goodbye"], ["Goodbye!", "See you later!", "Take care!"])
]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

#userinout preprocessing
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
        user_input = translator.translate(user_input, src=detected_lang, dest='en').text
    
    response = ''
    response = translator.translate(response, src='en', dest=detected_lang).text
    
    #websearch
    if not response:
        search_results = list(search(user_input, num=3, stop=3))
        if search_results:
            return f"Here are some search results for '{user_input}':\n" + "\n".join(search_results)

    return response

pdf_texts = load_pdfs()

# Main loop
while True:
    user_input = input("User: ")
    response = generate_response(user_input, pdf_texts)
    print("DOMA:", response)
