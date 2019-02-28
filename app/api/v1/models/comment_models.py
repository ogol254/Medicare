from datetime import datetime, timedelta

# local imports
from ....db_config import init_db
from .base_model import BaseModel


class CommentModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, created_by=123, comment="text"):
        """initialize the user model"""
        self.comment = comment
        self.created_by = created_by
        self.db = init_db()

    def save_comment(self):
        """Add user details to the database"""
        comment = {
            "comment": self.comment,
            "created_by": self.created_by
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO comments (comment, created_by) \
            VALUES (%(comment)s, %(created_by)s) RETURNING comment_id;
            """
        curr.execute(query, record)
        comment_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(comment_id)

    def get_specif_record_comments(self, record_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT comment_id, created_by, comment, created_on FROM comments WHERE record_id=%s;"""
        curr.execute(query, [record_id])
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            comment_id, created_by, comment, created_on = items

            comments = dict(
                comment_id=int(comment_id),
                comment=comment,
                created_by=BaseModel().get_name(created_by),
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(comments)
        return resp
