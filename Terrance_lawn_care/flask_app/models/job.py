from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

from flask import flash


class Job:
    db = "lawn_care_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.customer = data["customer"]
        self.location = data["location"]
        self.description = data["description"]
        self.date_performed = data["date_performed"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = None


    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO jobs (customer,location,description,date_performed,user_id)
                VALUES (%(customer)s,%(location)s,%(description)s,%(date_performed)s,%(user_id)s);
                """
        return connectToMySQL("lawn_care_schema").query_db(query,form_data)
    
    @classmethod
    def update(cls,data):
        query = """
                UPDATE jobs
                SET customer = %(customer)s,
                location = %(location)s,
                description = %(description)s ,
                date_performed = %(date_performed)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM jobs
                WHERE id = %(id)s;
                """
        return connectToMySQL("lawn_care_schema").query_db(query,data)
    
    @classmethod
    def get_all_jobs_with_users(cls):
        query = """
        SELECT * FROM jobs JOIN users ON jobs.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        job_object_list = []
        for each_job_dictionary in results:
            print(each_job_dictionary)
            new_job_object = cls(each_job_dictionary)
            new_user_dictionary = {
                "id": each_job_dictionary["users.id"],
                "first_name": each_job_dictionary["first_name"],
                "last_name": each_job_dictionary["last_name"],
                "email": each_job_dictionary["email"],
                "password": each_job_dictionary["password"],
                "created_at": each_job_dictionary["users.created_at"],
                "updated_at": each_job_dictionary["users.updated_at"],
            }
            new_user_object = user.User(new_user_dictionary)
            new_job_object.user = new_user_object
            job_object_list.append(new_job_object)
        return job_object_list

    @classmethod
    def get_one_job_with_user(cls, data):
        query = """
        SELECT * FROM jobs JOIN users ON jobs.user_id = users.id WHERE jobs.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        job_dictionary = results[0]
        new_job = cls(job_dictionary)
        new_user_dictionary = {
                "id": job_dictionary["users.id"],
                "first_name": job_dictionary["first_name"],
                "last_name": job_dictionary["last_name"],
                "email": job_dictionary["email"],
                "password": job_dictionary["password"],
                "created_at": job_dictionary["users.created_at"],
                "updated_at": job_dictionary["users.updated_at"],
            }
        user_object = user.User(new_user_dictionary)
        new_job.user = user_object
        return new_job

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM jobs
                JOIN users on jobs.user_id = users.id;
                """
        results = connectToMySQL("lawn_care_schema").query_db(query)
        jobs = []
        for row in results:
            this_job = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_job.user = user.User(user_data)
            jobs.append(this_job)
        return jobs
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM jobs
                JOIN users on jobs.user_id = users.id
                WHERE jobs.id = %(id)s;
                """
        result = connectToMySQL("lawn_care_schema").query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_job = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_job.user = user.User(user_data)
        return this_job
    
    @staticmethod
    def validate_job(form_data):
        is_valid = True

        if len(form_data['customer']) < 3:
            flash("Species must be at least 3 characters long.")
            is_valid = False
        if len(form_data['location']) < 3:
            flash("Location must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) > 50:
            flash("Description must be no more than 50 characters long.")
            is_valid = False
        if form_data['date_performed'] == '':
            flash("Please input a date.")
            is_valid = False

        return is_valid