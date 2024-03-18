from . import CONN, CURSOR
from models.customer import Customer
from models.restaurant import Restaurant
import sqlite3

class Review:
  all = {}
  
  def __init__(self, star_rating, customer_id, restaurant_id, id=None):
    self.id = id
    self.star_rating = star_rating
    self.customer_id = customer_id
    self.restaurant_id = restaurant_id
    
  @property
  def star_rating(self):
    return self._star_rating

  @star_rating.setter
  def star_rating(self, star_rating):
    if type(star_rating) is int and 0 <= star_rating <= 5:
      self._star_rating = star_rating
    else:
      raise ValueError("Values must be from 0 to 5")
  
  @property
  def customer_id(self):
        return self._customer_id
    
  @customer_id.setter
  def customer_id(self, customer_id):
        if type(customer_id) is int and Customer.find_by_id(customer_id):
            self._customer_id = customer_id
        else:
            raise ValueError("Customer_id must reference a customer in the database")
  
  @property
  def restaurant_id(self):
        return self._restaurant_id
    
  @restaurant_id.setter
  def restaurant_id(self, restaurant_id):
        if type(restaurant_id) is int and Restaurant.find_by_id(restaurant_id):
            self._restaurant_id = restaurant_id
        else:
            raise ValueError("Restaurant_id must reference a restaurant in the database")
  
  @classmethod
  def create_table(cls):
    sql = """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            star_rating INTEGER,
            customer_id INTEGER,
            restaurant_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
            UNIQUE(customer_id, restaurant_id)
        )
    """
    try:
        CURSOR.execute(sql)
        CONN.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
  
  def save(self):
    sql = """
            INSERT INTO reviews(star_rating, customer_id, restaurant_id)
            VALUES(?,?,?)
    """
    
    CURSOR.execute(sql, (self.star_rating, self.customer_id, self.restaurant_id))
    CONN.commit()
    
    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self
  
  @classmethod
  def create(cls, star_rating, customer_id, restaurant_id):
      review = cls(star_rating, customer_id, restaurant_id)
      review.save()
      return review
  
  @classmethod
  def instance_from_db(cls, row):
        review = cls.all.get(row[0])
        if review:
            review.star_rating = row[1]
            review.customer_id = row[2]
            review.restaurant_id = row[3]
        else:
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review
  
  @classmethod
  def get_all(cls):
        sql = """
                SELECT * 
                FROM reviews
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
  
  @classmethod
  def find_by_id(cls, id):
        sql = """
                SELECT *
                FROM reviews
                WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
  
  def review_customer(self):
    sql = """
        SELECT *
        FROM customers
        WHERE id = ?
    """
    row = CURSOR.execute(sql, (self.customer_id,)).fetchone()
    if row:
        # Check if the row contains valid data
        if row[1] and row[2]:  # Assuming first name is at index 1 and last name is at index 2
            return Customer(row[1], row[2])
        else:
            raise ValueError("Customer data retrieved from the database is invalid")
    else:
        return None
  
  def review_restaurant(self):
    sql = """
        SELECT *
        FROM restaurants
        WHERE id = ?
    """
    row = CURSOR.execute(sql, (self.restaurant_id,)).fetchone()
    if row:
        # Check if the row contains valid data
        if row[1] and row[2]:  # Assuming first name is at index 1 and last name is at index 2
            return Restaurant(row[1], row[2])
        else:
            raise ValueError("Restaurant data retrieved from the database is invalid")
    else:
        return None
    
  def full_review(self):
        # Retrieve the restaurant associated with the review
        restaurant = self.review_restaurant()
        
        # Retrieve the customer associated with the review
        customer = self.review_customer()
        
        # Format the review details into the desired string format
        review_string = f"Review for {restaurant.name} by {customer.customer_full_name()}: {self.star_rating} stars."
        
        return review_string
