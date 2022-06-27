from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import bcrypt
from flask import flash
import re  # the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Registration:
    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        # self.confirm_password = data['confirm_password']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']

    @classmethod
    def check_user(cls, data):
        print(data)
        query = "SELECT * FROM registrations WHERE email = %(email)s;"

        result = connectToMySQL("login_registration_schema").query_db(query, data)
        print(result)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM registrations WHERE id = %(id)s;"
        result = connectToMySQL("login_registration_schema").query_db(query, data)
        print(result)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    # Match w/ line 34 in controller, (create)
    def create(cls, data):
        query = "INSERT INTO registrations (f_name, l_name, email, password ) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password)s); "
        return connectToMySQL("login_registration_schema").query_db(query, data)
        # Return the id of the row i inserted into. well the model in controller is called, it returns ID

    @staticmethod
    def validate_login(login_creds):
        is_valid = True  # we assume this is true
        if len(login_creds['f_name']) < 2:
            flash("First Name must be at least 2 characters.", "f_name")
            is_valid = False
        if len(login_creds['l_name']) < 2:
            flash("Last name must be at least 2 characters.", "l_name")
            is_valid = False
        if len(login_creds['email']) < 2:
            flash("Email is not long enough.", "email")
            is_valid = False
        elif not EMAIL_REGEX.match(login_creds['email']):
            flash("Invalid email address!", "email")
            is_valid = False
        if len(login_creds['password']) < 2:
            flash("Password dont work", "password")
            is_valid = False
        elif login_creds["password"] != login_creds["confirm_password"]:
            flash("Password did not match", "password")
            is_valid = False
        # confirm pass
        return is_valid

    # @staticmethod
    # def validate_login


# +++++++ LOGIN +++++++

# class Login:
#     def __init__(self, data):
#         self.id = data('id')
#         self.email = data('email')
#         self.password = data('password')
