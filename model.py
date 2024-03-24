class Review:
    def __init__(self, id, description, sentiment):
        self.id = id
        self.description = description
        self.sentiment = sentiment


class ReviewList:
    def __init__(self):
        self.reviews = []

    # adiciona uma review à lista
    def add_review(self, description, sentiment):
        id = len(self.reviews) + 1
        review = Review(id, description, sentiment)
        self.reviews.append(review)

    # retorna a lista de reviews
    def get_reviews(self):
        return self.reviews

    # reinicia a lista de reviews
    def reset_reviews(self):
        self.reviews = []
