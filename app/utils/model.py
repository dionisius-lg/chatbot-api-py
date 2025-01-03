import pickle
import re
import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

class Model:
    def __init__(self, model_path=None, vectorizer_path=None):
        # init lemmatizer and model with vectorizer when exist
        self.lemmatizer = WordNetLemmatizer()
        self.model = None
        self.vectorizer = None
        if model_path and vectorizer_path:
            self.load_model(model_path, vectorizer_path)

    def lemmatize_sentence(self, sentence):
        # change sentence to base word (lemmatize)
        return " ".join([self.lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)])

    def train(self, intents):
        training_sentences = []
        training_labels = []

        # prepare data to train
        for intent in intents:
            for pattern in intent["patterns"]:
                lemmatized_sentence = self.lemmatize_sentence(pattern)
                training_sentences.append(lemmatized_sentence)
                training_labels.append(intent["tag"])

        # prepare vecorizer to change sentence to numeric feature
        self.vectorizer = CountVectorizer()
        training_vectors = self.vectorizer.fit_transform(training_sentences).toarray()

        # prepare classifier naive bayes
        self.model = MultinomialNB()
        self.model.fit(training_vectors, training_labels)

    def save_model(self, model_path, vectorizer_path):
        with open(model_path, "wb") as model_file:
            pickle.dump(self.model, model_file)

        with open(vectorizer_path, "wb") as vectorizer_file:
            pickle.dump(self.vectorizer, vectorizer_file)

    def load_model(self, model_path, vectorizer_path):
        with open(model_path, "rb") as model_file:
            self.model = pickle.load(model_file)

        with open(vectorizer_path, "rb") as vectorizer_file:
            self.vectorizer = pickle.load(vectorizer_file)

    def predict_class(self, text):
        lemmatized_text = self.lemmatize_sentence(text)
        text_vector = self.vectorizer.transform([lemmatized_text]).toarray()
        prediction = self.model.predict(text_vector)
        probabilities = self.model.predict_proba(text_vector)
        return prediction[0], probabilities[0]

    def get_response(self, predicted_class, user_input, probabilities, intents, threshold=0.6):
        # when predicted probabilities class lower than threshold, give fallback response
        if max(probabilities) < threshold:
            return "Saya tidak mengetahui yang Anda maksud."

        # when class match, process response
        for intent in intents:
            if intent["tag"] == predicted_class:
                print(predicted_class)
                # check if pattern has name to retrieve for greeting tag
                if predicted_class == "salam":
                    # use regex to extract name from pattern
                    match = re.search(r"(halo saya|nama saya) ([A-Za-z ]+)", user_input)

                    if match:
                        # name found
                        name = match.group(2)
                        name = f"{name}"
                        result = random.choice(intent["responses"]).format(name=name)
                        # return random.choice(intent["responses"]).format(name=name)
                    else:
                        result = random.choice(intent["responses"]).format(name="")
                        # print(qwe)
                        # return qwe
                        # return random.choice(intent["responses"]).format(name="")
                    
                    result = result.strip()
                    result = result.replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!")
                    result = re.sub(r'([,.?])\s+', r'\1 ', result)  # Put single space after punctuation
                    result = re.sub(r'\s+', ' ', result)
                    result = result.strip()
                    return result
                else:
                    # for tag except greeting, return random response
                    # Untuk tag selain greeting, langsung kembalikan respons acak
                    return random.choice(intent["responses"])

        return "Saya tidak mengetahui yang Anda maksud."