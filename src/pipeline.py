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


class Pipeline:
    def __init__(self, file_path=None):
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.classifier = None
        self.vectorizer3 = None
        self.file_path = file_path
        pass

    # Pré-processamento do texto
    def preprocess_text(self, text):

        # Converte para minúsculas
        text = text.lower()

        # expande contrações
        text = contractions.fix(text)

        # Remove pontuação
        text = ''.join(
            [char for char in text if char not in string.punctuation])

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        text = ' '.join([word for word in text.split()
                        if word.lower() not in stop_words])
        # Lematização

        lemmatizer = WordNetLemmatizer()
        text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

        # Remove pontuação novamente
        text = ''.join(
            [char for char in text if char not in string.punctuation])
        return text

    def save_model(self):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")
        joblib.dump(self.classifier, 'model.pkl')
        joblib.dump(self.vectorizer3,  'vectorizer.pkl')

    def load_model(self):
        self.classifier = joblib.load('model.pkl')
        self.vectorizer3 = joblib.load('vectorizer.pkl')

    # Treino do modelo
    def train_model(self, file_path):
        self.file_path = file_path
        df = pd.read_csv(self.file_path)

        # Pré-processamento dos dados
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

        # Divisão dos dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            bow3, labels, test_size=0.1)

        # Treino do modelo
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)

        self.classifier = classifier

    # Previsão do sentimento
    def predict_sentiment(self, text):
        if self.classifier is None or self.vectorizer3 is None:
            raise Exception(
                "Model not trained yet. Please run 'createmodel()' first.")

        # Pré-processamento da nova crítica
        preprocessed_text = self.preprocess_text(text)

        # Vetorização usando os mesmos vetores usados ​​no treinamento
        vectorized_text = self.vectorizer3.transform([preprocessed_text])

        # Faz a previsão
        prediction = self.classifier.predict(vectorized_text)
        return prediction
