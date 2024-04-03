import joblib
from textpreprocessor import TextPreprocessor

class Pipeline:
    def __init__(self):
        self.classifier = None
        self.vectorizer3 = None

    def load_model(self):
        self.classifier = joblib.load('model.pkl')
        self.vectorizer3 = joblib.load('vectorizer.pkl')

    def predict_sentiment(self, text):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")

        preprocessor = TextPreprocessor()

        text = preprocessor.remove_html_tags(text)
        text = preprocessor.remove_special_characters(text)
        text = preprocessor.remove_punctuation(text)
        text = preprocessor.remove_urls(text)
        text = preprocessor.remove_emojis(text)
        text = preprocessor.expand_chatwords(text)
        text = preprocessor.expand_contractions(text)
        text = preprocessor.to_lower(text)
        text = preprocessor.tokenize_text(text)
        text = preprocessor.remove_stopwords(text)
        text = preprocessor.lemmatize_tokens(text)

        vectorized_text = self.vectorizer3.transform([' '.join(text)])
        prediction = self.classifier.predict(vectorized_text)        
        return prediction
