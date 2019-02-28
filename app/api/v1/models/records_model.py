from datetime import datetime, timedelta

# local imports
from ....db_config import init_db
from .base_model import BaseModel


class RecordModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, incident_id=1, created_by=123, id_num=1234, location="location", type="type",
                 description="description", facility_id=1):
        """initialize the user model"""
        self.incident_id = incident_id
        self.created_by = created_by
        self.id_num = id_num
        self.type = type
        self.description = description
        self.location = location
        self.facility_id = facility_id
        self.db = init_db()

    def get_all(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT record_id, created_by, id_num, type, description, 
            location, facility_id, status, created_on FROM records;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            record_id, created_by, id_num, type, description, location, facility_id, status, created_on = items

            records = dict(
                record_id=int(record_id),
                created_by=BaseModel().get_name(created_by),
                name=BaseModel().get_name(id_num),
                type=type,
                description=description,
                location=location,
                facility_id=int(facility_id),
                status=status,
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(records)
        return resp

    def save(self):
        """Add user details to the database"""
        record = {
            "incident_id": self.incident_id,
            "created_by": self.created_by,
            "id_num": self.id_num,
            "type": self.type,
            "description": self.description,
            "location": self.location,
            "facility_id": self.facility_id,
            "status": "Created"
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO records (incident_id, created_by, id_num, type, description, location, \
            facility_id, status) \
            VALUES (%(incident_id)s, %(created_by)s, %(id_num)s,\
            %(type)s, %(description)s, %(location)s, %(facility_id)s, %(status)s) RETURNING record_id;
            """
        curr.execute(query, record)
        record_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(record_id)

    def get_single_records(self, record_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT record_id, created_by, id_num, type, description, 
            location, facility_id, status, created_on FROM records;""")
        data = curr.fetchone()[0]
        resp = []
        curr.close()

        record_id, created_by, id_num, type, description, location, facility_id, status, created_on = data

        records = dict(
            record_id=int(record_id),
            created_by=BaseModel().get_name(created_by),
            name=BaseModel().get_name(id_num),
            type=type,
            description=description,
            location=location,
            facility_id=int(facility_id),
            status=status,
            created_on=created_on.strftime("%B %d, %Y")
        )
        resp.append(records)
        return resp
