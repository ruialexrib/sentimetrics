# This file contains the classes that represent the data model of the application.
# The Review class represents a single review, and the ReviewList class represents a list of reviews.
# The ReviewList class also contains methods to add a review to the list, get the list of reviews, and reset the list of reviews.

# Review class
# This class represents a single review. It has three attributes: id, description, and sentiment.
# The id attribute is a unique identifier for the review, the description attribute is the text of the review, and the sentiment attribute is the sentiment of the review (positive or negative).
# The class has a constructor that initializes the id, description, and sentiment attributes.
# The class does not have any methods other than the constructor, as it is a simple data class.
class Review:
    def __init__(self, id, description, sentiment):
        self.id = id
        self.description = description
        self.sentiment = sentiment

# ReviewList class
# This class represents a list of reviews. It has one attribute: reviews, which is a list of Review objects.
# The class has a constructor that initializes the reviews attribute to an empty list.
# The class has three methods: add_review, get_reviews, and reset_reviews.
# The add_review method takes a description and sentiment as input, creates a new Review object with a unique id, and adds it to the reviews list.
# The get_reviews method returns the list of reviews.
# The reset_reviews method resets the list of reviews to an empty list.
# The ReviewList class is used to manage the list of reviews in the application.
# It provides methods to add, get, and reset the reviews, and encapsulates the logic for managing the list of reviews.
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
