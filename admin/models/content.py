from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SiteContent(db.Model):
    __tablename__ = 'site_content'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section': self.section,
            'key': self.key,
            'value': self.value
        }
