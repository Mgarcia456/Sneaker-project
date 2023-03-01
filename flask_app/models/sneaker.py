from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user

class Sneaker:
    def __init__(self,data):
        self.id = data['id']
        self.brand = data['brand']
        self.model = data['model']
        self.size = data['size']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
#           create a sneaker
    @classmethod
    def create(cLs,data):
        query = """
        INSERT INTO sneakers (brand, model, size, price, user_id) 
        VALUES (%(brand)s, %(model)s, %(size)s, %(price)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
        ## read all           
    @classmethod
    def get_all(cLs):
        query = """
        SELECT * FROM sneakers
        JOIN users
        ON users.id = recipes.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print("RESULTS========>\n\n", results)
        all_sneakers = []
        if results:
            for row in results:
            # create a sneaker
                this_sneaker = cLs(row)
            # create owner of sneaker
            # prepare the dict for user 
                user_data ={
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['updated_at']
              }
                # make the user
                this_seller = user.User(user_data)
                # add new attribute
                this_sneaker.seller = this_seller
                all_sneakers.append(this_sneaker)
        return all_sneakers
    #   get by id
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM sneakers
        JOIN users
        ON users.id = sneakers.user_id
        WHERE sneakers.id = %(id)s ;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print("????????", results)
        if results:
            this_sneaker = cls(results[0])
            row = results[0]
            user_data ={
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['updated_at']
            }
            this_user = user.User(user_data)
            this_sneaker.seller = this_user
            return this_sneaker
        return False
    #      update method
    @classmethod
    def update(cLs,data):
        query = """
        UPDATE sneakers
        SET 
        brand = %(brand)s,
        model = %(model)s,
        size = %(size)s,
        price = %(price)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    ##       delete method
    @classmethod
    def delete(cLs,data):
        query = """
        DELETE FROM sneakers
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#    validator
    @staticmethod
    def vaildator(form_data):
        is_valid =  True
        if len(form_data['brand']) < 1:
            is_valid = False
            flash("what brand?")
        if len(form_data['model']) < 1:
            is_valid = False
            flash("what model?")
        if len(form_data['size']) < 1:
            is_valid = False
            flash("what size is the shoe")
        if len(form_data['price']) < 1:
            is_valid = False
            flash("target price?")
        return is_valid