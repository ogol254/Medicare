from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AuthModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, id_number="12345678", first_name="first", address="address",
                 last_name="last", password="pass", tell="1234567890"):
        """initialize the user model"""
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.tell = tell
        self.address = address
        self.db = init_db()

    def get_user_by_id(self, id_num):
        """return user from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT first_name, last_name, password, id_num, role \
            FROM users WHERE id_num = '%s'""" % (id_num))
        data = curr.fetchone()
        curr.close()
        return data

    # def save_user(self):
    #     """Add user details to the database"""
    #     user = {
    #         "username": self.username,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "email": self.email,
    #         "password": self.password,
    #         "isadmin": True
    #     }
    #     # check if user exists
    #     if BaseModel().check_exists(table="users", field="username", data=user['username']):
    #         return False
    #     database = self.db
    #     curr = database.cursor()
    #     query = """INSERT INTO users (first_name, last_name, username, email, password, is_admin) \
    #         VALUES ( %(first_name)s, %(last_name)s,\
    #         %(username)s, %(email)s, %(password)s, %(isadmin)s) RETURNING username;
    #         """
    #     curr.execute(query, user)
    #     username = curr.fetchone()[0]
    #     database.commit()
    #     curr.close()
    #     return ("{} saved sucessfully".format(username))

    def logout_user(self, token):
        """This function logs out a user by adding thei token to the blacklist table"""
        conn = self.db
        curr = conn.cursor()
        query = """
                INSERT INTO blacklist 
                VALUES (%(tokens)s) RETURNING tokens;
                """
        inputs = {"tokens": token}
        curr.execute(query, inputs)
        blacklisted_token = curr.fetchone()[0]
        conn.commit()
        curr.close()
        return blacklisted_token
