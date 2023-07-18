from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import job
from flask import flash

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "lawn_care_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.jobs = []


    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        located_user = cls(results[0])
        return located_user

    @classmethod
    def get_user_with_jobs(cls,data):
        query = "SELECT * FROM users LEFT JOIN jobs ON users.id = jobs.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('arbortrary_schema').query_db(query, data)
        user_dictionary = results[0]
        user_object = cls(user_dictionary)
        for current_job_dictionary in results:
            if current_job_dictionary['jobs.id'] == None:
                break
            print(current_job_dictionary)
            new_job_dictionary = {
                "id": current_job_dictionary["jobs.id"],
                "customer": current_job_dictionary["customer"],
                "location": current_job_dictionary["location"],
                "description": current_job_dictionary["description"],
                "date_performed": current_job_dictionary["date_performed"],
                "created_at": current_job_dictionary["jobs.created_at"],
                "updated_at": current_job_dictionary["jobs.updated_at"]
            }
            new_job_object = job.Job(new_job_dictionary)
            user_object.jobs.append(new_job_object)
            return user_object

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN jobs ON users.id = jobs.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('lawn_care_schema').query_db(query, data)
        user = cls(results[0])
        for row in results:
            if row['jobs.id'] == None:
                break
            data = {
                "id": row["jobs.id"],
                "customer": row["customer"],
                "location": row["location"],
                "description": row["description"],
                "date_performed": row["date_performed"],
                "created_at": row["jobs.created_at"],
                "updated_at": row["jobs.updated_at"]
            }
            user.jobs.append(job.Job(data))
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","signup")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","signup")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","signup")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","signup")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","signup")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","signup")
            is_valid = False
        return is_valid