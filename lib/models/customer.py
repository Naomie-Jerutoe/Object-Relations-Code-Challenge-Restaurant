from . import CONN, CURSOR
import sqlite3

class Customer:
  all = {}
  
  def __init__(self, first_name, last_name, id=None):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
  
  @property
  def first_name(self):
    return self._first_name 
  
  @first_name.setter
  def first_name(self, first_name):
    if isinstance(first_name, str) and len(first_name):
      self._first_name = first_name
    else:
      raise ValueError("First Name must be a non-empty string")
  
  @property
  def last_name(self):
    return self._last_name 
  
  @last_name.setter
  def last_name(self, last_name):
    if isinstance(last_name, str) and len(last_name):
      self._last_name = last_name
    else:
      raise ValueError("Last Name must be a non-empty string")
  
  @classmethod
  def create_table(cls):
    sql = """
            CREATE TABLE IF NOT EXISTS customers(
              id INTEGER PRIMARY KEY,
              first_name TEXT,
              last_name TEXT)
    """
    CURSOR.execute(sql)
    CONN.commit()
  
  def save(self):
    sql = """
            INSERT INTO customers(first_name, last_name)
            VALUES(?,?)
    """
    
    CURSOR.execute(sql, (self.first_name, self.last_name))
    CONN.commit()
    
    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self
  
  @classmethod
  def create(cls, first_name, last_name):
    customer = cls(first_name, last_name)
    customer.save()
    return customer
  
  @classmethod
  def instance_from_db(cls, row):
    customer = cls.all.get(row[0])
    if customer:
      customer.first_name = row[1]
      customer.last_name = row[2]
    else:
      customer = cls(row[1], row[2])
      customer.id = row[0]
      cls.all[customer.id] = customer
    return customer
  
  @classmethod
  def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM customers
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
  
  def customer_reviews(self):
        from models.review import Review
        sql = """
            SELECT *
            FROM reviews
            WHERE customer_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()

        # Map each row to a Review instance
        reviews = [Review.instance_from_db(row) for row in rows]
        return reviews
  
  def customer_restaurants(self):
        from models.restaurant import Restaurant
        sql = """
            SELECT *
            FROM restaurants AS r
            INNER JOIN reviews AS rv ON r.id = rv.restaurant_id
            WHERE rv.customer_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()

        # Map each row to a Restaurant instance
        restaurants = [Restaurant.instance_from_db(row) for row in rows]
        return restaurants
  
  def customer_full_name(self):
    return f"{self.first_name} {self.last_name}"
  
  def customer_favourite_restaurant(self):
        # Retrieve all reviews left by this customer
        customer_reviews = self.customer_reviews()

        # If the customer has no reviews, return None
        if not customer_reviews:
            return None

        # Find the review with the highest star rating
        highest_rating = max(customer_reviews, key=lambda review: review.star_rating)

        # Return the restaurant associated with the highest-rated review
        return highest_rating.review_restaurant()
  
  def customer_add_review(self, restaurant_id, rating):
    from models.review import Review
    new_review = Review.create(rating, self.id, restaurant_id)
    return new_review
  
  def customer_delete_reviews(self, restaurant_id):
        sql = """
            DELETE FROM reviews
            WHERE customer_id = ? AND restaurant_id = ?
        """
        try:
            CURSOR.execute(sql, (self.id, restaurant_id))
            CONN.commit()
            print("Reviews deleted successfully.")
        except sqlite3.Error as e:
            print("An error occurred while deleting reviews:", e)