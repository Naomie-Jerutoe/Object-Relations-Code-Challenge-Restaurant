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

    # Create instances of Customer and Restaurant
    # customer1 = Customer.create("Naomie", "Lagat")
    # customer2 = Customer.create("Collins", "Bett")
    # customer3 = Customer.create("John", "Jing")
    # customer4 = Customer.create("Joy", "Jeng")
    # customer5 = Customer.create("Bella", "Blonde")
    # customer6 = Customer.create("Tenda", "Wema")
    # sarova = Restaurant.create("Sarova", 15000)
    # jamia = Restaurant.create("Jamia", 14150)
    # highland = Restaurant.create("Highland", 14300)
    # diamond = Restaurant.create("Diamond", 25502)

    #  Get IDs of the created customers and restaurants
    # customer1_id = customer1.id
    # customer2_id = customer2.id
    # customer3_id = customer3.id
    # customer4_id = customer4.id
    # customer5_id = customer5.id
    # customer6_id = customer6.id
    # sarova_id = sarova.id
    # jamia_id = jamia.id
    # highland_id = highland.id
    # diamond_id = diamond.id

    # Create instances of Review using the IDs of associated customers and restaurants
    # Review.create(4, customer1_id, jamia_id)
    # Review.create(3, customer2_id, sarova_id)
    # Review.create(5, customer3_id, highland_id)
    # Review.create(4, customer6_id, 3)
    # Review.create(2, 4, 1)
    
    # instance1 Review.create(4, customer4_id, sarova_id)
    # restaurant_instance = instance1.review_restaurant()
    # if restaurant_instance:
    #     print("Restaurant:", restaurant_instance.name, restaurant_instance.price)
    # else:
    #     print("No restaurant found for this review.")
    
    # instance2 Review.create(2, customer5_id, diamond_id)  # Create a Review instance
    # customer_instance = instance2.review_customer()  # Call the method
    # if customer_instance:
    #     print("Customer:", customer_instance.first_name, customer_instance.last_name)
    # else:
    #     print("No customer found for this review.")
    print("Restaurant Reviews Management")
    print()

def customer_methods_tests():
    #display full name of a customer
    print("*******Customer's Full Name********")
    customer = Customer.find_by_id(1)
    display_name = customer.customer_full_name()
    print(display_name)
    print()
    
    #display customers favorite restaurant
    print("*******Customer's Favourite Restaurant********")
    favorite = customer.customer_favourite_restaurant()
    if favorite:
        print(f"Favorite Restaurant: {favorite.name}")
    else:
        print("Favorite Restaurant: None")
    print()
    
    #display customer add review
    # print("*******Customer's Added Review********")
    # customer5 = Customer.find_by_id(5)
    # new_review = customer5.customer_add_review(1, 1)
    # print("Successfully ")
    # print()
    
    #delete a review
    # print("*******Customer's Deleted Review********")
    # deleted_review = customer5.customer_delete_reviews
    # print("Review deleted successfully")
    # print()

def restaurant_methods_tests():
    #display the fanciest restaurant
    print("*******Fanciest Restaurant********")
    fanciest_restaurant = Restaurant.restaurant_fanciest()
    print(f"Fanciest Restaurant: {fanciest_restaurant.name}")
    print()
    
    #display all reviews of a certain restaurant
    print("*******All Reviews of a specific Restaurant********")
    restaurant = Restaurant.find_by_id(1)
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
    print()

def review_methods_tests():
    #display full review of a restaurant
    print("*******Full Review of a Restaurant********")
    review = Review.find_by_id(1)
    if review:
        formatted_review = review.full_review()
        print(formatted_review)
    else:
        print("Review not found.")
    print()


if __name__ == "__main__":
    main()
    customer_methods_tests()
    restaurant_methods_tests()
    review_methods_tests()
