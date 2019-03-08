from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


from ....db_config import init_db
from .base_model import BaseModel


class IncidentModel(BaseModel):
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
        curr.execute("""SELECT incident_id, created_by, type, description, 
            location, status, assigned_to, tell, comment, created_on FROM incidents;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            incident_id, created_by, type, description, location, status, assigned_to, tell, comment, created_on = items
            if assigned_to is not None:
                assigned_to = BaseModel().get_name(assigned_to)
            incidents = dict(
                incident_id=int(incident_id),
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
            resp.append(incidents)
        return resp

    def get_with_status(self, status):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT incident_id, created_by, type, description, location,
            assigned_to, tell, comment, created_on FROM incidents WHERE status=%s;"""
        curr.execute(query, [status])
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            incident_id, created_by, type, description, location, assigned_to, tell, comment, created_on = items
            if assigned_to is not None:
                assigned_to = BaseModel().get_name(assigned_to)
            incidents = dict(
                incident_id=int(incident_id),
                reported_by=created_by,
                type=type,
                description=description,
                location=location,
                tell=tell,
                comment=comment,
                assigned_to=assigned_to,
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(incidents)
        return resp

    def save(self):
        """Add user details to the database"""
        incident = {
            "name": self.name,
            "location": self.location,
            "type": self.type,
            "description": self.description,
            "status": "Draft",
            "tell": self.tell
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO incidents (created_by, location, type, description, status, tell) \
            VALUES ( %(name)s, %(location)s,\
            %(type)s, %(description)s, %(status)s, %(tell)s) RETURNING incident_id;
            """
        curr.execute(query, incident)
        incident_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(incident_id)

    def update_status(self, status, incident_id):
        """Add user details to the database"""

        resp = BaseModel().update_item(table="incidents",
                                       field="status",
                                       data=status,
                                       item_field="incident_id",
                                       item_id=incident_id)

        return resp

    def get_single_incidents(self, incident_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT incident_id, created_by, type, description, location, status,  
            assigned_to, tell, comment, created_on FROM incidents WHERE incident_id=%s"""
        curr.execute(query, [incident_id])
        data = curr.fetchone()
        resp = []
        curr.close()

        incident_id, created_by, type, description, location, status, assigned_to, tell, comment, created_on = data
        if assigned_to is not None:
            assigned_to = BaseModel().get_name(assigned_to)
        incidents = dict(
            incident_id=int(incident_id),
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
        resp.append(incidents)
        return resp


class UserIncidentsModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, id_num):
        """initialize the user model"""
        self.id = id_num
        self.db = init_db()

    def get_all_incident_assigned_to(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT incident_id, created_by, type, description, location, status, tell, 
            comment, created_on FROM incidents WHERE assigned_to=%s;"""
        curr.execute(query, [self.id])
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            incident_id, created_by, type, description, location, status, tell, comment, created_on = items
            
            incidents = dict(
                incident_id=int(incident_id),
                reported_by=created_by,
                type=type,
                description=description,
                location=location,
                status=status,
                tell=int(tell),
                comment=comment,
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(incidents)
        return resp
