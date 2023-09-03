from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models.customer import Customer
from app.models.restaurant import Restaurant
from app.models.review import Review

# Database setup
DATABASE_URL = "my.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_customer(first_name, last_name):
    customer = Customer(first_name=first_name, last_name=last_name)
    session.add(customer)
    session.commit()
    return customer

def create_restaurant(name, price):
    restaurant = Restaurant(name=name, price=price)
    session.add(restaurant)
    session.commit()
    return restaurant

def create_review(star_rating, comment, customer, restaurant):
    review = Review(star_rating=star_rating, comment=comment, customer=customer, restaurant=restaurant)
    session.add(review)
    session.commit()
    return review

def main():
    try:
        # Create customers
        customer1 = create_customer("John", "Doe")
        customer2 = create_customer("Alice", "Smith")

        # Create restaurants
        restaurant1 = create_restaurant("Sample Restaurant 1", 3)
        restaurant2 = create_restaurant("Sample Restaurant 2", 2)

        # Create reviews
        create_review(4, "Great food!", customer1, restaurant1)
        create_review(3, "Good service.", customer2, restaurant1)
        create_review(5, "Excellent!", customer1, restaurant2)

        # Query customers
        customers = session.query(Customer).all()
        print("All Customers:")
        for customer in customers:
            print(f"Customer: {customer.first_name} {customer.last_name}")

        # Query restaurants
        restaurants = session.query(Restaurant).order_by(Restaurant.price.desc()).all()
        print("\nRestaurants Ordered by Price (Descending):")
        for restaurant in restaurants:
            print(f"Restaurant: {restaurant.name}, Price: {restaurant.price}")

        # Query reviews for a specific restaurant
        restaurant_reviews = session.query(Review).filter_by(restaurant=restaurant1).all()
        print("\nReviews for Restaurant 1:")
        for review in restaurant_reviews:
            print(f"Review for {review.restaurant.name} by {review.customer.full_name()}: {review.star_rating} stars")

        # Test relationship loading
        customer1_reviews = customer1.reviews
        print("\nReviews by Customer 1:")
        for review in customer1_reviews:
            print(f"Review for {review.restaurant.name}: {review.star_rating} stars")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
