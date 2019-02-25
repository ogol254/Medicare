from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AuthModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, id_number="12345678", password="pass"):
        """initialize the user model"""
        self.id_number = id_number
        self.password = generate_password_hash(password)
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
