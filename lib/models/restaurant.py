from . import CONN, CURSOR

class Restaurant:
  all = {}
  
  def __init__(self, name, price, id=None):
    self.id = id
    self.name = name
    self.price = price
    
  def __repr__(self):
    return f"Restaurant(id={self.id}, name='{self.name}', price={self.price})"
  
  @property
  def name(self):
    return self._name 
  
  @name.setter
  def name(self, name):
    if isinstance(name, str) and len(name):
      self._name = name
    else:
      raise ValueError("Name must be a non-empty string")
  
  @property
  def price(self):
    return self._price
  
  @price.setter
  def price(self, price):
    if isinstance(price, int) and price > 0:
      self._price = price
  
  @classmethod
  def create_table(cls):
    sql = """
            CREATE TABLE IF NOT EXISTS restaurants(
              id INTEGER PRIMARY KEY,
              name TEXT,
              price INTEGER)
    """
    CURSOR.execute(sql)
    CONN.commit()
  
  def save(self):
    sql = """
            INSERT INTO restaurants(name, price)
            VALUES(?,?)
    """
    
    CURSOR.execute(sql, (self.name, self.price))
    CONN.commit()
    
    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self
  
  @classmethod
  def create(cls, name, price):
    restaurant = cls(name, price)
    restaurant.save()
    return restaurant
  
  @classmethod
  def instance_from_db(cls, row):
    restaurant = cls.all.get(row[0])
    if restaurant:
      restaurant.name = row[1]
      restaurant.price = row[2]
    else:
      restaurant = cls(row[1], row[2])
      restaurant.id = row[0]
      cls.all[restaurant.id] = restaurant
    return restaurant

  @classmethod
  def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM restaurants
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
  
  def restaurant_reviews(self):
    from models.review import Review
    sql = """
            SELECT *
            FROM reviews
            WHERE restaurant_id = ?
    """
    rows = CURSOR.execute(sql, (self.id,)).fetchall()
    reviews = [Review.instance_from_db(row) for row in rows]
    return reviews
  
  def restaurant_customers(self):
        from models.customer import Customer
        sql = """
            SELECT *
            FROM customers AS c
            INNER JOIN reviews AS rv ON c.id = rv.customer_id
            WHERE rv.restaurant_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Customer.instance_from_db(row) for row in rows]
  
  @classmethod
  def restaurant_fanciest(cls):
    sql = """
            SELECT *
            FROM restaurants
            ORDER BY price DESC
            LIMIT 1
    """
    row = CURSOR.execute(sql).fetchone()
    return cls.instance_from_db(row) if row else None
  
  def restaurant_all_reviews(self):
        # Retrieve all reviews associated with the restaurant
        reviews = self.restaurant_reviews()
        
        # Initialize an empty list to store reviews list strings
        reviews_list = []
        
        # Format each review into the desired string format
        for review in reviews:
            # Retrieve the customer associated with the review
            customer = review.review_customer()
            
            # Format the review details into the desired string format
            review_string = f"Review for {self.name} by {customer.customer_full_name()}: {review.star_rating} stars."
            
            # Append the formatted review string to the list
            reviews_list.append(review_string)
        return reviews_list