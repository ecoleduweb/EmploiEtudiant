from app import db

class StudyProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Program('{self.id}', '{self.name}')"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "name": self.name
        }