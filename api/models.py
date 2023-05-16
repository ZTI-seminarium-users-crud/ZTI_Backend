from api import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    specialization = db.Column(db.String)
    degree = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    is_male = db.Column(db.Boolean)
    average_grade = db.Column(db.Float)
    hair_color = db.Column(db.String)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    age = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialization": self.specialization,
            "degree": self.degree,
            "semester": self.semester,
            "is_male": self.is_male,
            "average_grade": self.average_grade,
            "hair_color": self.hair_color,
            "height": self.height,
            "weight": self.weight,
            "age": self.age
        }