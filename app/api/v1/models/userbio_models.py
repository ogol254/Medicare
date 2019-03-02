from ....db_config import init_db
from .base_model import BaseModel


class UserBioModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, id_number="12345678", date_of_birth=""):
        """initialize the user model"""
        self.id_number = id_number
        self.date_of_birth = date_of_birth
        self.db = init_db()

    def save(self):
        """Add user details to the database"""
        user = {
            "id_number": self.id_number,
            "data_of_birth": self.date_of_birth
        }
        # check if user exists
        if BaseModel().check_exists(table="users", field="id_num", data=user['id_number']) == False:
            return None

        if BaseModel().check_exists(table="bio", field="id_number", data=user['id_number']) == True:
            return False

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO bio (id_number, date_of_birth) \
            VALUES ( %(id_number)s, %(data_of_birth)s) RETURNING id_number;
            """
        curr.execute(query, user)
        id_num = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(id_num)

    def get_user_bio(self, id_number):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT date_of_birth, blood_group, email, weight, height, secondary_tell
                FROM bio WHERE id_number=%s"""
        curr.execute(query, [id_number])
        data = curr.fetchone()
        curr.close()

        if not data:
            return False

        date_of_birth, blood_group, email, weight, height, secondary_tell = data
        user_data = {
            "id_number": int(id_number),
            "name": BaseModel().get_name(id_number),
            "date_of_birth": date_of_birth,
            "blood_group": blood_group,
            "email": email,
            "weight": weight,
            "height": height,
            "secondary_tell": secondary_tell
        }
        return user_data
