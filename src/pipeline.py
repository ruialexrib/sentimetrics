import string
import nltk
import contractions
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
import joblib


# Pipeline class
# This class represents the pipeline for training and using the sentiment analysis model.
# It has several methods for preprocessing the text, training the model, saving and loading the model, and making predictions.
# The class has a constructor that initializes the file_path attribute to None.
# The class has a preprocess_text method that preprocesses the text by converting it to lowercase, expanding contractions, removing punctuation and stopwords, and lemmatizing the text.
# The class has a save_model method that saves the trained model to disk.
# The class has a load_model method that loads the trained model from disk.
# The class has a train_model method that trains the sentiment analysis model using the data from the specified file.
# The class has a predict_sentiment method that predicts the sentiment of a given text using the trained model.
# The Pipeline class encapsulates the logic for training and using the sentiment analysis model.
# It provides methods for preprocessing the text, training the model, saving and loading the model, and making predictions.
class Pipeline:
    def __init__(self, file_path=None):
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.classifier = None
        self.vectorizer3 = None
        self.file_path = file_path
        pass

    # text preprocessing
    def preprocess_text(self, text):
            
        # converts text to lowercase
        text = text.lower()

        # expands contractions
        text = contractions.fix(text)

        # removes punctuation
        text = ''.join(
            [char for char in text if char not in string.punctuation])

        # removes stopwords
        stop_words = set(stopwords.words('english'))
        text = ' '.join([word for word in text.split()
                        if word.lower() not in stop_words])
        
        # lemmatization
        lemmatizer = WordNetLemmatizer()
        text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

        # removes punctuation again
        text = ''.join(
            [char for char in text if char not in string.punctuation])
        
        # returns the preprocessed text
        return text

    # saves the trained model to disk
    def save_model(self):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")
        joblib.dump(self.classifier, 'model.pkl')
        joblib.dump(self.vectorizer3,  'vectorizer.pkl')

    # loads the trained model from disk
    def load_model(self):
        self.classifier = joblib.load('model.pkl')
        self.vectorizer3 = joblib.load('vectorizer.pkl')

    # trains the sentiment analysis model using the data from the specified file
    def train_model(self, file_path):
        self.file_path = file_path
        df = pd.read_csv(self.file_path)

        # text preprocessing
        df["Text"] = df["Text"].apply(self.preprocess_text)
        df = df.dropna()

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        bow = vectorizer.fit_transform(df['Text'])
        labels = df['Sentiment']

        # Feature selection
        vectorizer2 = TfidfVectorizer(min_df=10)
        bow2 = vectorizer2.fit_transform(df['Text'])
        selected_features = SelectKBest(chi2, k='all').fit(
            bow2, labels).get_support(indices=True)
        bestfeatures = [vectorizer2.get_feature_names_out()[t]
                        for t in selected_features]
        vectorizer3 = TfidfVectorizer(min_df=10, vocabulary=bestfeatures)
        self.vectorizer3 = vectorizer3
        bow3 = self.vectorizer3.fit_transform(df['Text'])

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            bow3, labels, test_size=0.1)

        # Training the model
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)

        self.classifier = classifier

    # predicts the sentiment of a given text using the trained model
    def predict_sentiment(self, text):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")

        # text preprocessing
        preprocessed_text = self.preprocess_text(text)

        # vectorization
        vectorized_text = self.vectorizer3.transform([preprocessed_text])

        # prediction
        prediction = self.classifier.predict(vectorized_text)
        
        # returns the prediction
        return prediction
