from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class UserModel(BaseModel):
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

    def get_users(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT id_num, first_name, last_name, address, tell FROM users;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            id_num, first_name, last_name, address, tell = items
            users = dict(
                id_number=int(id_num),
                first_name=first_name,
                last_name=last_name,
                address=address,
                tell=tell
            )
            resp.append(users)
        return resp

    def get_specific_user(self, id_num):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT id_num, first_name, last_name, address, tell, role FROM users WHERE id_num=%s """
        curr.execute(query, [id_num])
        data = curr.fetchall()
        resp = []
        curr.close()

        id_num, first_name, last_name, address, tell, role = data
        users = dict(
            id_number=int(id_num),
            first_name=first_name,
            last_name=last_name,
            address=address,
            tell=tell,
            role=role
        )
        resp.append(users)
        return resp

    def save(self):
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
            return False

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (first_name, last_name, id_num, address, role, password, tell) \
            VALUES ( %(first_name)s, %(last_name)s,\
            %(id_number)s, %(address)s, %(role)s, %(password)s, %(tell)s) RETURNING id_num;
            """
        curr.execute(query, user)
        id_num = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(id_num)
