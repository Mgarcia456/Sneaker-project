from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
#       creat a user==========================
    @classmethod
    def create(cLs, data):
      query = """
        INSERT INTO users (first_name, last_name, email ,password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
      """
      return connectToMySQL(DATABASE).query_db(query,data)
#          get one user            
    @classmethod
    def get_by_id(cLs, data):
      query = """
        SELECT * FROM users 
        WHERE users.id = %(id)s;
      """
      results = connectToMySQL(DATABASE).query_db(query,data)
      print(results)
      if len(results) < 1: return False
      return cLs(results[0])
#    get one by email      
    @classmethod
    def get_by_email(cLs, data):
      query = """
        SELECT * FROM users 
        WHERE users.email = %(email)s;
      """
      results = connectToMySQL(DATABASE).query_db(query,data)
      print(results)
      if len(results) < 1: return False
      return cLs(results[0])




      #       user validate=======
    @staticmethod
    def validate(data):
      is_valid = True

      if len(data['first_name']) < 1:
          is_valid = False
          flash("first_name is required!")

      if len(data['last_name']) < 1:
          is_valid = False
          flash("last_name is required!")

      if len(data['email']) < 1:
          is_valid = False
          flash("email is required!")
      elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
      else:
          data_for_email = {
            'email': data['email']
          }
          potential_user = User.get_by_email(data_for_email)
          if potential_user:
            is_valid = False
            flash("email already taken")

      if len(data['password']) < 1:
          is_valid = False
          flash("password is required!")
      elif not data['password'] == data['confirm_password']:
          is_valid = False
          flash("password dont match!")

      return is_valid