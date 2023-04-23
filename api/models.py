from api import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    specialization = db.Column(db.String)
    degree = db.Column(db.String)
    semester = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialization": self.specialization,
            "degree": self.degree,
            "semester": self.semester
        }