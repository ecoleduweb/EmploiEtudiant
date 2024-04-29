from app import db

class EmploymentSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"EmploymentSchedule(id={self.id}, description={self.description})"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "description": self.description
        }