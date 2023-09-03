from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
# from .base import Base  # Assuming you have a common base class for your models

class Restaurant():
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    cuisine = Column(String)

    # Define the relationship with the Review model (one-to-many)
    reviews = relationship('Review', back_populates='restaurant')

    # Returns the average star rating for the restaurant
    def average_rating(self):
        if not self.reviews:
            return 0  # Handle the case where there are no reviews
        total_rating = sum(review.star_rating for review in self.reviews)
        return total_rating / len(self.reviews)

    # Returns the date of the latest review for the restaurant
    def latest_review_date(self):
        if not self.reviews:
            return None
        return max(review.date for review in self.reviews)

    # Returns a list of customers who reviewed the restaurant
    def get_reviewing_customers(self):
        return [review.customer for review in self.reviews]

    # Returns the most recent reviews for the restaurant
    def get_recent_reviews(self, limit):
        return sorted(self.reviews, key=lambda review: review.date, reverse=True)[:limit]

    # Returns reviews by star rating within a given range
    def get_reviews_by_rating(self, min_rating, max_rating):
        return [review for review in self.reviews if min_rating <= review.star_rating <= max_rating]

    # Returns reviews within a specified date range
    def get_reviews_by_date(self, start_date, end_date):
        return [review for review in self.reviews if start_date <= review.date <= end_date]

    # Returns the total count of reviews for the restaurant
    def get_review_count(self):
        return len(self.reviews)

    # Returns a summary of the restaurant's reviews
    def get_review_summary(self):
        total_reviews = len(self.reviews)
        if total_reviews == 0:
            return "No reviews available."
        
        average_rating = self.average_rating()
        return f"Total Reviews: {total_reviews}, Average Rating: {average_rating:.2f}"

    # Returns the most recent review with a comment for the restaurant
    def get_highest_rated_review_with_comment(self):
        reviews_with_comments = [review for review in self.reviews if review.comment]
        if not reviews_with_comments:
            return None
        return max(reviews_with_comments, key=lambda review: review.star_rating)

    # Returns the lowest-rated review for the restaurant
    def get_lowest_rated_review(self):
        if not self.reviews:
            return None
        return min(self.reviews, key=lambda review: review.star_rating)

    # Returns a list of customers who reviewed the restaurant
    def get_reviewed_customers(self):
        return [review.customer for review in self.reviews]

    # Returns reviews with comments for the restaurant
    def get_reviews_with_comments(self):
        return [review for review in self.reviews if review.comment]

    # Returns reviews for a specific cuisine for the restaurant
    def get_reviews_for_cuisine(self, cuisine):
        return [review for review in self.reviews if review.customer.cuisine == cuisine]

    # Returns the average review length (number of characters) for the restaurant
    def get_average_review_length(self):
        if not self.reviews:
            return 0  # Handle the case where there are no reviews
        total_length = sum(len(review.comment) for review in self.reviews if review.comment)
        return total_length / len(self.reviews)

    # Returns popular times based on review timestamps for the restaurant
    def get_popular_times(self):
        if not self.reviews:
            return None
        
        # Sample logic: Group reviews by hour of the day
        review_hours = [review.date.hour for review in self.reviews]
        popular_times = dict((hour, review_hours.count(hour)) for hour in set(review_hours))
        
        return popular_times

    # Returns reviews grouped by star rating for the restaurant
    def get_reviews_grouped_by_rating(self):
        rating_counts = {}
        for review in self.reviews:
            rating = review.star_rating
            if rating in rating_counts:
                rating_counts[rating] += 1
            else:
                rating_counts[rating] = 1
        return rating_counts

    # Returns reviews with specific keywords for the restaurant
    def get_reviews_with_keywords(self, keywords):
        return [review for review in self.reviews if any(keyword in review.comment for keyword in keywords)]

    # Returns reviews sorted by date for the restaurant
    def get_reviews_sorted_by_date(self, descending=True):
        return sorted(self.reviews, key=lambda review: review.date, reverse=descending)

    # Returns the average rating for a specific cuisine for the restaurant
    def get_average_rating_for_cuisine(self, cuisine):
        cuisine_reviews = [review for review in self.reviews if review.restaurant.cuisine == cuisine]
        if not cuisine_reviews:
            return 0  # Handle the case where there are no reviews for the cuisine
        total_rating = sum(review.star_rating for review in cuisine_reviews)
        return total_rating / len(cuisine_reviews)