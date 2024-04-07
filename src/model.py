# Review class to store the review details
class Review:
    def __init__(self, id, description, sentiment):
        self.id = id
        self.description = description
        self.sentiment = sentiment

# ReviewList class to store the list of reviews
class ReviewList:
    def __init__(self):
        self.reviews = []

    # adds a review to the list
    def add_review(self, description, sentiment):
        id = len(self.reviews) + 1
        review = Review(id, description, sentiment)
        self.reviews.append(review)

    # returns the list of reviews
    def get_reviews(self):
        return self.reviews

    # resets the list of reviews
    def reset_reviews(self):
        self.reviews = []
