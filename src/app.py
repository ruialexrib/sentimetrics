from flask import Flask, render_template, request, redirect, url_for
from model import ReviewList
from pipeline import Pipeline

# Define o caminho do arquivo de dados
file_path = 'data/data.csv'

# Inicializa a lista de reviews
reviews_list = ReviewList()

# Inicializa o pipeline
pipeline = Pipeline(file_path)

# Carrega o modelo
pipeline.load_model()

# adiciona 2 exemplos de reviews


def add_example_reviews():
    example_reviews = [
        ("Overall a great experience.",),
        ("It was so bad I had lost the heart to finish it.",)
    ]
    for review_text, in example_reviews:
        sentiment = pipeline.predict_sentiment(review_text)[0]
        reviews_list.add_review(review_text, sentiment)


add_example_reviews()

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


@app.route('/train/<model_name>')
def train(model_name):
    # Rotas para treinar o modelo
    file_path = f'data/{model_name}'
    print("Treinando o modelo", file_path)
    pipeline.train_model(file_path)
    pipeline.save_model()
    pipeline.load_model()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Inicia o servidor Flask
    print("Servidor a correr em http://localhost:8082")
    app.run(host="0.0.0.0", port=8082, debug=True)
