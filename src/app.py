from flask import Flask, render_template, request, redirect, url_for
from model import ReviewList
from pipeline import Pipeline
from werkzeug.utils import secure_filename
import os
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
reviews_list = ReviewList()
pipeline = Pipeline()
pipeline.load_model()

example_reviews = [
    ("I absolutely loved this movie! The acting was superb and the storyline kept me engaged from start to finish.",),
    ("I was extremely disappointed by this movie. The plot was weak and the acting was subpar.",)
]
for review_text, in example_reviews:
    sentiment = pipeline.predict_sentiment(review_text)[0]
    reviews_list.add_review(review_text, sentiment)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = ''
app.config['ALLOWED_EXTENSIONS'] = {'pkl'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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


@app.route('/')
def index():
    reviews = reviews_list.get_reviews()
    return render_template('index.html', reviews=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    description = request.form['description']
    sentiment = pipeline.predict_sentiment(description)[0]
    reviews_list.add_review(description, sentiment)
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    reviews_list.reset_reviews()
    return redirect(url_for('index'))


@app.route('/restart', methods=['GET'])
def restart():
    pipeline.load_model()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("Servidor a correr em http://localhost:8082")
    app.run(host="0.0.0.0", port=8082, debug=True)
