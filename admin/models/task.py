from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='waiting')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'urgency': self.urgency,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status
        }
