from flask import Flask, render_template, request, redirect, url_for
from model import ReviewList
from pipeline import Pipeline
from werkzeug.utils import secure_filename
import os
import nltk

# Download NLTK resources
def download_nltk_resources():
    resources = ['punkt', 'wordnet', 'stopwords', 'averaged_perceptron_tagger']
    for resource in resources:
        if not nltk.download(resource, quiet=True):
            print(f"Resource '{resource}' downlaoded successfully.")
        else:
            print(f"Resource '{resource}' already exists.")

# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Download NLTK resources
download_nltk_resources()

# Create a ReviewList and Pipeline object
reviews_list = ReviewList()
pipeline = Pipeline()

# Load the model
pipeline.load_model()

# Add some example reviews
example_reviews = [
    ("I absolutely loved this movie! The acting was superb and the storyline kept me engaged from start to finish.",),
    ("I was extremely disappointed by this movie. The plot was weak and the acting was subpar.",)
]

# Predict sentiment for the example reviews and add them to the list
for review_text, in example_reviews:
    sentiment = pipeline.predict_sentiment(review_text)[0]
    reviews_list.add_review(review_text, sentiment)

# Create a Flask app
app = Flask(__name__)

# Set the upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = ''
app.config['ALLOWED_EXTENSIONS'] = {'pkl'}

# Route to upload a file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', message=f"Error: Invalid file format. Only {app.config['ALLOWED_EXTENSIONS']} files are allowed")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', message=f"Upload do ficheiro {filename} efetuado com sucesso.")
        else:
            return render_template('upload.html', message=f"Error: Invalid file format. Only {app.config['ALLOWED_EXTENSIONS']} files are allowed")
    return render_template('upload.html')

# Route to display the index page
@app.route('/')
def index():
    reviews = reviews_list.get_reviews()
    return render_template('index.html', reviews=reviews)


# Route to add a review
@app.route('/add_review', methods=['POST'])
def add_review():
    description = request.form['description']
    sentiment = pipeline.predict_sentiment(description)[0]
    reviews_list.add_review(description, sentiment)
    return redirect(url_for('index'))

# Route to reset the reviews
@app.route('/reset', methods=['POST'])
def reset():
    reviews_list.reset_reviews()
    return redirect(url_for('index'))

# Route to restart the model
@app.route('/restart', methods=['GET'])
def restart():
    pipeline.load_model()
    return redirect(url_for('index'))

# start the server
if __name__ == '__main__':
    print("Server running at http://localhost:8082")
    app.run(host="0.0.0.0", port=8082, debug=True)
