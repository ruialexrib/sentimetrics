import re
import emoji
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        self.contractions_dict = {
            "ain't": "is not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'd've": "he would have",
            "he'll": "he will",
            "he'll've": "he will have",
            "he's": "he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how is",
            "i'd": "I would",
            "i'd've": "I would have",
            "i'll": "I will",
            "i'll've": "I will have",
            "i'm": "I am",
            "i've": "I have",
            "isn't": "is not",
            "it'd": "it would",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she would",
            "she'd've": "she would have",
            "she'll": "she will",
            "she'll've": "she will have",
            "she's": "she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so is",
            "that'd": "that would",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there would",
            "there'd've": "there would have",
            "there's": "there is",
            "they'd": "they would",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what will",
            "what'll've": "what will have",
            "what're": "what are",
            "what's": "what is",
            "what've": "what have",
            "when's": "when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where is",
            "where've": "where have",
            "who'll": "who will",
            "who'll've": "who will have",
            "who's": "who is",
            "who've": "who have",
            "why's": "why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you would",
            "you'd've": "you would have",
            "you'll": "you will",
            "you'll've": "you will have",
            "you're": "you are",
            "you've": "you have"
        }
        self.chat_words = {
            "AFAIK": "As Far As I Know",
            "AFK": "Away From Keyboard",
            "ASAP": "As Soon As Possible",
            "ATK": "At The Keyboard",
            "ATM": "At The Moment",
            "A3": "Anytime, Anywhere, Anyplace",
            "BAK": "Back At Keyboard",
            "BBL": "Be Back Later",
            "BBS": "Be Back Soon",
            "BFN": "Bye For Now",
            "B4N": "Bye For Now",
            "BRB": "Be Right Back",
            "BRT": "Be Right There",
            "BTW": "By The Way",
            "B4": "Before",
            "B4N": "Bye For Now",
            "CU": "See You",
            "CUL8R": "See You Later",
            "CYA": "See You",
            "FAQ": "Frequently Asked Questions",
            "FC": "Fingers Crossed",
            "FWIW": "For What It's Worth",
            "FYI": "For Your Information",
            "GAL": "Get A Life",
            "GG": "Good Game",
            "GN": "Good Night",
            "GMTA": "Great Minds Think Alike",
            "GR8": "Great!",
            "G9": "Genius",
            "IC": "I See",
            "ICQ": "I Seek you (also a chat program)",
            "ILU": "ILU: I Love You",
            "IMHO": "In My Honest/Humble Opinion",
            "IMO": "In My Opinion",
            "IOW": "In Other Words",
            "IRL": "In Real Life",
            "KISS": "Keep It Simple, Stupid",
            "LDR": "Long Distance Relationship",
            "LMAO": "Laugh My A.. Off",
            "LOL": "Laughing Out Loud",
            "LTNS": "Long Time No See",
            "L8R": "Later",
            "MTE": "My Thoughts Exactly",
            "M8": "Mate",
            "NRN": "No Reply Necessary",
            "OIC": "Oh I See",
            "PITA": "Pain In The A..",
            "PRT": "Party",
            "PRW": "Parents Are Watching",
            "QPSA?": "Que Pasa?",
            "ROFL": "Rolling On The Floor Laughing",
            "ROFLOL": "Rolling On The Floor Laughing Out Loud",
            "ROTFLMAO": "Rolling On The Floor Laughing My A.. Off",
            "SK8": "Skate",
            "STATS": "Your sex and age",
            "ASL": "Age, Sex, Location",
            "THX": "Thank You",
            "TTFN": "Ta-Ta For Now!",
            "TTYL": "Talk To You Later",
            "U": "You",
            "U2": "You Too",
            "U4E": "Yours For Ever",
            "WB": "Welcome Back",
            "WTF": "What The F...",
            "WTG": "Way To Go!",
            "WUF": "Where Are You From?",
            "W8": "Wait...",
            "7K": "Sick:-D Laugher",
            "TFW": "That feeling when",
            "MFW": "My face when",
            "MRW": "My reaction when",
            "IFYP": "I feel your pain",
            "TNTL": "Trying not to laugh",
            "JK": "Just kidding",
            "IDC": "I don't care",
            "ILY": "I love you",
            "IMU": "I miss you",
            "ADIH": "Another day in hell",
            "ZZZ": "Sleeping, bored, tired",
            "WYWH": "Wish you were here",
            "TIME": "Tears in my eyes",
            "BAE": "Before anyone else",
            "FIMH": "Forever in my heart",
            "BSAAW": "Big smile and a wink",
            "BWL": "Bursting with laughter",
            "BFF": "Best friends forever",
            "CSL": "Can't stop laughing"
        }
        self.additional_html_terms = [
            'br', 'hr', 'a', 'img', 'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'u', 'i', 'b', 'ul', 'ol', 'li', 'table', 'tr', 'th', 'td', 'tbody',
            'thead', 'tfoot', 'blockquote', 'code', 'pre', 'q', 'cite', 'abbr', 'acronym',
            'address', 'article', 'aside', 'audio', 'bdi', 'bdo', 'canvas', 'caption', 'col',
            'colgroup', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dl', 'dt', 'figcaption',
            'figure', 'footer', 'header', 'kbd', 'legend', 'main', 'map', 'mark', 'meter', 'nav',
            'noscript', 'object', 'optgroup', 'option', 'output', 'progress', 'rp', 'rt', 'ruby',
            's', 'samp', 'section', 'select', 'small', 'source', 'strong', 'sub', 'summary', 'sup',
            'time', 'title', 'track', 'var', 'video', 'wbr'
        ]

    def to_lower(self, text):
        return text.lower()

    def expand_contractions(self, text):
        expanded_text = ' '.join(self.contractions_dict.get(
            word, word) for word in text.split())
        return expanded_text

    def remove_html_tags(self, text):
        additional_terms_pattern = '|'.join(
            re.escape(term) for term in self.additional_html_terms)
        regex_pattern = rf'<(?:[^>]*?|({additional_terms_pattern}))>'
        clean_text = re.sub(regex_pattern, '', text)
        return clean_text

    def remove_urls(self, text):
        return re.sub(r'http\S+', '', text)

    def remove_special_characters(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def remove_punctuation(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def remove_emojis(self, text):
        return emoji.demojize(text, delimiters=(" ", " "))

    def expand_chatwords(self, text):
        expanded_text = ' '.join(self.chat_words.get(word, word)
                                 for word in text.split())
        return expanded_text

    def correct_spelling(self, text):
        return TextBlob(text).correct()

    def tokenize_text(self, text):
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        return tokens

    def remove_stopwords(self, tokens):
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [
            token for token in tokens if token.lower() not in stop_words]
        return filtered_tokens

    def stem_tokens(self, tokens):
        porter = PorterStemmer()
        stemmed_tokens = [porter.stem(token) for token in tokens]
        return stemmed_tokens

    def lemmatize_tokens(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens

    def replace_synonyms(self, tokens):
        synonyms_replaced = []
        for token in tokens:
            synonyms = []
            for syn in wordnet.synsets(token):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())
            if synonyms:
                synonyms_replaced.append(synonyms[0])  # Use the first synonym
            else:
                synonyms_replaced.append(token)
        return synonyms_replaced

    def count_tokens(self, text_column):
        total_tokens = 0
        for text in text_column:
            if isinstance(text, list):
                text = ' '.join(text)
            elif not isinstance(text, str):
                raise ValueError(
                    "Unsupported data type. Only lists and strings are supported.")

            tokens = word_tokenize(text)
            total_tokens += len(tokens)

        return total_tokens
