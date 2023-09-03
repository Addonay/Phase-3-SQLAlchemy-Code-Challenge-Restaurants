from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from review import Review  # Import the Review model
# from .base import Base  # Assuming you have a common base class for your models

class Customer():
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with the Review model (one-to-many)
    reviews = relationship('Review', back_populates='customer')

    # Returns the full name of the customer
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Returns the restaurant with the highest average rating among reviewed restaurants
    def get_highest_rated_restaurant(self):
        restaurants = self.get_reviewed_restaurants()
        if not restaurants:
            return None
        return max(restaurants, key=lambda restaurant: restaurant.average_rating())

    # Returns the date of the latest review by the customer
    def latest_review_date(self):
        if not self.reviews:
            return None
        return max(review.date for review in self.reviews)

    # Returns the customer's favorite restaurant based on average ratings
    def favorite_restaurant(self):
        return self.get_highest_rated_restaurant()

    # Adds a review for a restaurant and associates it with the customer
    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        return new_review
    
    # Returns all reviews by the customer for a specific restaurant
    def get_reviews_for_restaurant(self, restaurant):
        return [review for review in self.reviews if review.restaurant == restaurant]
    
    # Deletes all reviews by the customer for a specific restaurant
    def delete_reviews(self, restaurant):
        restaurant_reviews = self.get_reviews_for_restaurant(restaurant)
        for review in restaurant_reviews:
            self.reviews.remove(review)

    # Returns reviews by star rating within a given range
    def get_reviews_by_rating(self, min_rating, max_rating):
        return [review for review in self.reviews if min_rating <= review.star_rating <= max_rating]

    # Returns reviews within a specified date range
    def get_reviews_by_date(self, start_date, end_date):
        return [review for review in self.reviews if start_date <= review.date <= end_date]

    # Returns the total count of reviews by the customer
    def get_review_count(self):
        return len(self.reviews)

    # Returns a summary of the customer's reviews
    def get_review_summary(self):
        total_reviews = len(self.reviews)
        if total_reviews == 0:
            return "No reviews available."
        
        average_rating = self.average_rating()
        return f"Total Reviews: {total_reviews}, Average Rating: {average_rating:.2f}"

    # Returns the most recent reviews by the customer
    def get_recent_reviews(self, limit):
        return sorted(self.reviews, key=lambda review: review.date, reverse=True)[:limit]

    # Returns the restaurants reviewed by the customer
    def get_reviewed_restaurants(self):
        return [review.restaurant for review in self.reviews]

    # Returns the customer's favorite cuisine based on reviewed restaurants
    def get_favorite_cuisine(self):
        if not self.reviews:
            return None
    
        # Create a dictionary to store the total rating for each cuisine
        cuisine_ratings = {}
    
        for review in self.reviews:
            restaurant = review.restaurant
            cuisine = restaurant.cuisine
            rating = review.star_rating
    
            if cuisine in cuisine_ratings:
                cuisine_ratings[cuisine] += rating
            else:
                cuisine_ratings[cuisine] = rating
    
        # Find the cuisine with the highest total rating
        favorite_cuisine = max(cuisine_ratings, key=cuisine_ratings.get)
    
        return favorite_cuisine

    # Returns reviews by the customer for a specific cuisine
    def get_reviews_for_cuisine(self, cuisine):
        return [review for review in self.reviews if review.restaurant.cuisine == cuisine]

    # Returns reviews with comments by the customer
    def get_reviews_with_comments(self):
        return [review for review in self.reviews if review.comment]

    # Calculates and returns the average rating of the customer's reviews
    def average_rating(self):
        if not self.reviews:
            return 0  # Handle the case where there are no reviews
        total_rating = sum(review.star_rating for review in self.reviews)
        return total_rating / len(self.reviews)

    # Returns the highest-rated review by the customer
    def get_highest_rated_review(self):
        return max(self.reviews, key=lambda review: review.star_rating)

    # Returns the lowest-rated review by the customer
    def get_lowest_rated_review(self):
        return min(self.reviews, key=lambda review: review.star_rating)

    # Returns the count of unique reviewed restaurants by the customer
    def get_reviewed_restaurant_count(self):
        return len(set(review.restaurant for review in self.reviews))

    # Returns the reviewed restaurants sorted by rating or date
    def get_reviewed_restaurants_sorted(self, by_rating=True, descending=True):
        if by_rating:
            return sorted(self.get_reviewed_restaurants(), key=lambda restaurant: restaurant.average_rating(), reverse=descending)
        else:
            return sorted(self.get_reviewed_restaurants(), key=lambda restaurant: restaurant.latest_review_date(), reverse=descending)

    # Returns the most active period based on review dates
    def get_most_active_period(self):
        if not self.reviews:
            return None
        
        review_dates = [review.date for review in self.reviews]
        active_period = max(set(review_dates), key=review_dates.count)
        return active_period
