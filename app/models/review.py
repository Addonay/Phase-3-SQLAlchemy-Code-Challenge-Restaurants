from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from .base import Base  # Assuming you have a common base class for your models
from datetime import datetime

class Review():
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    comment = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    # Define foreign key relationships
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    # Define relationships with Customer and Restaurant models
    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    # Returns the customer associated with this review
    def get_customer(self):
        return self.customer

    # Returns the restaurant associated with this review
    def get_restaurant(self):
        return self.restaurant

    # Returns the age of the review in days
    def get_review_age(self):
        now = datetime.utcnow()
        age = (now - self.date).days
        return age

    # Returns the length of the review (number of characters)
    def get_review_length(self):
        return len(self.comment)

    # Returns the sentiment of the review (example implementation)
    def get_sentiment(self):
        # Replace with your NLP sentiment analysis logic
        # For simplicity, we assume positive sentiment for star ratings >= 4
        if self.star_rating >= 4:
            return "Positive"
        elif self.star_rating <= 2:
            return "Negative"
        else:
            return "Neutral"

    # Returns a summary of the review
    def get_review_summary(self):
        return f"Rating: {self.star_rating}, Comment: {self.comment}"

    # Checks if it's a positive review (threshold is 3 by default)
    def is_positive_review(self, threshold=3):
        return self.star_rating >= threshold

    # Gets related reviews based on similarity (example implementation)
    def get_related_reviews(self, similarity_threshold=0.7):
        # Replace with your text similarity algorithm
        # For simplicity, we return reviews with similar star ratings
        similar_reviews = [review for review in self.restaurant.reviews if abs(review.star_rating - self.star_rating) <= 1]
        return similar_reviews

    # Gets keywords in the comment
    def get_keywords_in_comment(self):
        # Replace with your keyword extraction logic (e.g., using NLP libraries)
        # For simplicity, we split the comment into words
        return self.comment.split()

    # Returns the word count of the comment
    def get_comment_word_count(self):
        return len(self.comment.split())

    # Returns the character count of the comment
    def get_comment_char_count(self):
        return len(self.comment)

    # Checks if it's a recent review (threshold is 30 days by default)
    def is_recent_review(self, days_threshold=30):
        now = datetime.utcnow()
        age = (now - self.date).days
        return age <= days_threshold

    # Returns the reviewer's location
    def get_reviewer_location(self):
        return self.customer.location if self.customer.location else "Location not provided"

    # Returns the reviewer's age (example implementation)
    def get_reviewer_age(self):
        if self.customer.date_of_birth:
            birth_year = self.customer.date_of_birth.year
            current_year = datetime.utcnow().year
            age = current_year - birth_year
            return age
        else:
            return "Age not provided"

    # Returns the reviewer's profile URL (example implementation)
    def get_reviewer_profile_url(self):
        return f"/profile/{self.customer.id}"  # Replace with your profile URL logic

    # Returns the number of upvotes for the review (example implementation)
    def get_review_upvotes(self):
        return self.upvotes if hasattr(self, 'upvotes') else 0  # Replace with your upvotes logic