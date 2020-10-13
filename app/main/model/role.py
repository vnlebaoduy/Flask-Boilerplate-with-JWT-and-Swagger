from .. import db, flask_bcrypt

class Role(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description =db.Column(db.String(255), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)



