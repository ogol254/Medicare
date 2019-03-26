from datetime import datetime, timedelta

# local imports
from ....db_config import init_db
from .base_model import BaseModel


class FacilityModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, name="name", location="location", created_by="created_by",
                 contact="0790463533", level="level 1"):
        """initialize the user model"""
        self.name = name
        self.location = location
        self.created_by = created_by
        self.contact = contact
        self.level = level
        self.db = init_db()

    def get_all(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT facility_id, name, location, created_by, 
                        contact, level FROM facilities;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            facility_id, name, location, created_by, contact, level = items

            facilities = dict(
                facility_id=int(facility_id),
                name=name,
                location=location,
                contact=contact,
                level=level,
                created_by=BaseModel().get_name(created_by)
            )
            resp.append(facilities)
        return resp

    def save_facility(self):
        """Add user details to the database"""
        facility = {
            "name": self.name,
            "location": self.location,
            "created_by": self.created_by,
            "contact": self.contact,
            "level" : self.level
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO facilities (name, location, created_by, contact, level) \
            VALUES ( %(name)s, %(location)s, %(created_by)s, %(contact)s, %(level)s) RETURNING facility_id;
            """
        curr.execute(query, facility)
        facility_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(facility_id)

    def get_single_facility(self, facility_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT facility_id, name, location, created_by, 
                        contact, level FROM facilities WHERE facility_id=%s"""
        curr.execute(query, [facility_id])
        data = curr.fetchone()
        resp = []
        curr.close()

        facility_id, name, location, created_by, contact, level = data

        facilities = dict(
            facility_id=int(facility_id),
            name=name,
            location=location,
            contact=contact,
            level=level,
            created_by=BaseModel().get_name(created_by)
        )
        resp.append(facilities)
        return resp
