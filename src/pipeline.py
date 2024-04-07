import joblib
from textpreprocessor import TextPreprocessor

# Pipeline class to load the model and vectorizer and predict sentiment
class Pipeline:
    def __init__(self):
        self.classifier = None
        self.vectorizer3 = None

    # load the model and vectorizer
    def load_model(self):
        self.classifier = joblib.load('model.pkl')
        self.vectorizer3 = joblib.load('vectorizer.pkl')

    # predict sentiment
    def predict_sentiment(self, text):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")

        preprocessor = TextPreprocessor()

        operations = [
            'remove_html_tags',
            'remove_urls',
            'remove_emojis',
            'expand_contractions',
            'expand_chatwords',
            'remove_special_characters',
            'remove_punctuation',
            'to_lower',
            'expand_emotions',
            'tokenize_text',
            'remove_stopwords',
            'lemmatize_tokens',
        ]
        
        for operation in operations:
            text = getattr(preprocessor, operation)(text)

        vectorized_text = self.vectorizer3.transform([' '.join(text)])
        prediction = self.classifier.predict(vectorized_text)
        return prediction
