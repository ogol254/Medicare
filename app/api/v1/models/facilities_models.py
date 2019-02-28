from datetime import datetime, timedelta

# local imports
from ....db_config import init_db
from .base_model import BaseModel


class FacilitiesModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, name="name", location="location", type="type",
                 description="description", tell=790463533):
        """initialize the user model"""
        self.name = name
        self.location = location
        self.type = type
        self.description = description
        self.tell = tell
        self.db = init_db()

    def get_all(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT facility_id, created_by, type, description, 
            location, status, assigned_to, tell, comment, created_on FROM facilities;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            facility_id, created_by, type, description, location, status, assigned_to, tell, comment, created_on = items
            if assigned_to != None:
                _n = BaseModel().get_user_by_id(assigned_to)
                assigned_to = _n[0] + ' ' + _n[1]
            facilities = dict(
                facility_id=int(facility_id),
                reported_by=created_by,
                type=type,
                description=description,
                location=location,
                status=status,
                tell=int(tell),
                comment=comment,
                assigned_to=assigned_to,
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(facilities)
        return resp

    def save(self):
        """Add user details to the database"""
        facility = {
            "name": self.name,
            "location": self.location,
            "type": self.type,
            "description": self.description,
            "status": "Draft",
            "tell": self.tell
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO facilities (created_by, location, type, description, status, tell) \
            VALUES ( %(name)s, %(location)s,\
            %(type)s, %(description)s, %(status)s, %(tell)s) RETURNING facility_id;
            """
        curr.execute(query, facility)
        facility_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(facility_id)

    def update_status(self, status, facility_id):
        """Add user details to the database"""

        resp = BaseModel().update_item(table="facilities",
                                       field="status",
                                       data=status,
                                       item_field="facility_id",
                                       item_id=facility_id)

        return resp

    def get_single_facilities(self, facility_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT facility_id, created_by, type, description, location, status,  
            assigned_to, tell, comment, created_on FROM facilities WHERE facility_id=%s"""
        curr.execute(query, [facility_id])
        data = curr.fetchone()
        resp = []
        curr.close()

        facility_id, created_by, type, description, location, status, assigned_to, tell, comment, created_on = data
        if assigned_to != None:
            _n = BaseModel().get_user_by_id(assigned_to)
            assigned_to = _n[0] + ' ' + _n[1]

        facilities = dict(
            facility_id=int(facility_id),
            reported_by=created_by,
            type=type,
            description=description,
            location=location,
            status=status,
            tell=int(tell),
            comment=comment,
            assigned_to=assigned_to,
            created_on=created_on.strftime("%B %d, %Y")
        )
        resp.append(facilities)
        return resp
