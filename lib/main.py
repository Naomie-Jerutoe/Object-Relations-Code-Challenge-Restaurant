#!/usr/bin/env python3
from models.__init__ import CURSOR, CONN
from models.customer import Customer
from models.restaurant import Restaurant
from models.review import Review

def main():
    # Create tables if they don't exist
    # Customer.create_table()
    # Restaurant.create_table()
    # Review.create_table()
  
    # # Create instances of Customer and Restaurant
    # customer1 = Customer.create("Naomie", "Lagat")
    # customer2 = Customer.create("Collins", "Bett")
    # customer3 = Customer.create("John", "Jing")
    # customer4 = Customer.create("Joy", "Jeng")
    # customer5 = Customer.create("Bella", "Blonde")
  
    # sarova = Restaurant.create("Sarova", 15000)
    # jamia = Restaurant.create("Jamia", 14150)
    # highland = Restaurant.create("Highland", 14300)
    # diamond = Restaurant.create("Diamond", 25502)
  
    # # Get IDs of the created customers and restaurants
    # customer1_id = customer1.id
    # customer2_id = customer2.id
    # customer3_id = customer3.id
    # customer4_id = customer4.id
    # customer5_id = customer5.id
    
    # sarova_id = sarova.id
    # jamia_id = jamia.id
    # highland_id = highland.id
    # diamond_id = diamond.id
  
    # # Create instances of Review using the IDs of associated customers and restaurants
    # Review.create(4, customer1_id, jamia_id)
    # Review.create(3, customer2_id, sarova_id)
    # Review.create(5, customer3_id, highland_id)
    
    # instance1 = Review.create(4, customer4_id, sarova_id)
    # restaurant_instance = instance1.review_restaurant()
    # if restaurant_instance:
    #     print("Restaurant:", restaurant_instance.name, restaurant_instance.price)
    # else:
    #     print("No restaurant found for this review.")
    
    # instance2 = Review.create(2, customer5_id, diamond_id)  # Create a Review instance
    # customer_instance = instance2.review_customer()  # Call the method
    # if customer_instance:
    #     print("Customer:", customer_instance.first_name, customer_instance.last_name)
    # else:
    #     print("No customer found for this review.")
    
    # customer = Customer.find_by_id(4)
    # deleted_review = customer.customer_delete_reviews(3)
    # print(deleted_review)
    
    # if new_review:
    #     print("New review created:")
    #     print("Review ID:", new_review.id)
    #     print("Star Rating:", new_review.star_rating)
    #     print("Customer ID:", new_review.customer_id)
    #     print("Restaurant ID:", new_review.restaurant_id)
    # else:
    #     print("Failed to create a new review.")
    
    # review = Review.find_by_id(1)
    # if review:
    #     formatted_review = review.full_review()
    #     print(formatted_review)
    # else:
    #     print("Review not found.")
        
    restaurant = Restaurant.find_by_id(2)
    if restaurant:
        formatted_reviews = restaurant.restaurant_all_reviews()
        
        if formatted_reviews:
            print("All Reviews for", restaurant.name)
            for review in formatted_reviews:
                print("-", review)
        else:
            print("No reviews found for", restaurant.name)
    else:
        print("Restaurant not found.")
        
if __name__ == "__main__":
    main()
