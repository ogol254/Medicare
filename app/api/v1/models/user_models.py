from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AuthModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, id_number="12345678", first_name="first", address="address",
                 last_name="last", password="pass", tell="1234567890", role="normal"):
        """initialize the user model"""
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.tell = tell
        self.role = role
        self.address = address
        self.db = init_db()

    def save_user(self):
        """Add user details to the database"""
        user = {
            "id_number": self.id_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "password": self.password,
            "role": self.role,
            "tell": self.tell
        }
        # check if user exists
        if BaseModel().check_exists(table="users", field="id_num", data=user['id_number']):
            return "User with ID {} exists".format(self.id_number)

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (first_name, last_name, id_num, address, role, password, tell) \
            VALUES ( %(first_name)s, %(last_name)s,\
            %(id_number)s, %(address)s, %(role)s, %(password)s, %(tell)s,) RETURNING id_num;
            """
        curr.execute(query, user)
        id_num = curr.fetchone()[0]
        database.commit()
        curr.close()
        return id_num
