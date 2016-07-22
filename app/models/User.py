from system.core.model import Model
import re
email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def login(self, data):
        query = "SELECT * FROM users WHERE email = :email"
        values = {"email": data["email"]}
        user_info = self.db.query_db(query, values)
        user_info = user_info[0]
        if user_info:
            if self.bcrypt.check_password_hash(user_info["pw_hash"], data["password"]):
                return {"id": user_info["id"], "first_name": user_info["first_name"]}
        return False

    def register(self, data):
        success = True
        errors = []
        query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        values = {"email": data["email"]}
        dupe = self.db.query_db(query, values)
        if dupe:
            errors.append("Email already in use")
            success = False
        if not data["first_name"] or len(data["first_name"]) < 2:
            errors.append("Name fields must be at least 2 characters")
            success = False
        elif not data["last_name"] or len(data["last_name"]) < 2:
            errors.append("Name fields must be at least 2 characters")
            success = False
        if not data["first_name"].isalpha() or not data["last_name"].isalpha():
            errors.append("Name fields can only contain alpha characters")
            success = False
        if not email_regex.match(data["email"]):
            success = False
            errors.append("Email invalid.")
        if data["password"] != data["conf_pw"]:
            errors.append("Passwords do not match")
            success = False
        if len(data["password"]) < 8:
            errors.append("Passwords must be a minimum of 8 characters")
            success = False
        if not success:
            return {"status": success, "errors": errors}
        hashed_pw = self.bcrypt.generate_password_hash(data["password"])
        query = "INSERT into users (first_name, last_name, email, pw_hash, created_at, updated_at) values(:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"
        data = {"first_name": data["first_name"], "last_name": data["last_name"], "email": data["email"], "pw_hash": hashed_pw}
        id = self.db.query_db(query, data)
        return {"status": True, "id": id, "first_name": data["first_name"]}

    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """