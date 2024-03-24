from flask import Flask, render_template, request, redirect, url_for
from model import ReviewList
from pipeline import Pipeline

# Define o caminho do arquivo de dados
file_path = 'data/data.csv'

# Inicializa a lista de reviews
reviews_list = ReviewList()

# Inicializa o pipeline
pipeline = Pipeline(file_path)

# Cria o modelo
#pipeline.train_model()

# Salva o modelo
#pipeline.save_model()

# Carrega o modelo
pipeline.load_model()

# adiciona 2 exemplos de reviews
review1 = "Overall a great experience."
review2 = "It was so bad  I had lost the heart to finish it."
sentiment1 = pipeline.predict_sentiment(review1)[0]
sentiment2 = pipeline.predict_sentiment(review2)[0]
reviews_list.add_review(review1, sentiment1)
reviews_list.add_review(review2, sentiment2)

# Inicializa a aplicação Flask
app = Flask(__name__)


@app.route('/')
def index():
    # Rota para a página inicial
    reviews = reviews_list.get_reviews()
    return render_template('index.html', reviews=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    # Rota para adicionar uma review
    description = request.form['description']
    sentiment = pipeline.predict_sentiment(description)[0]
    reviews_list.add_review(description, sentiment)
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    # Rota para reiniciar a lista de reviews
    reviews_list.reset_reviews()
    return redirect(url_for('index'))

@app.route('/train/<model_name>')  # <model_name> captura o nome do modelo na URL
def train(model_name):
    file_path = f'data/{model_name}'
    print("Treinando o modelo", file_path)
    pipeline.train_model(file_path)
    pipeline.save_model()
    return redirect(url_for('index'))