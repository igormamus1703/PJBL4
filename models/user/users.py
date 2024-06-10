from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__= "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column( db.Integer, db.ForeignKey(Role.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    password= db.Column(db.String(256) , nullable=False)

    role = db.relationship('Role', backref='users')

    @staticmethod
    def save_user(role_type_, username, email,password):
        role = Role.get_single_role(role_type_)
        user = User(role_id = role.id, username = username, email = email,
                    password = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_users():
        return User.query.all()
    
    @staticmethod
    def get_user_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            return user
        #return None
    
    @staticmethod
    def validate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if(user==None or not check_password_hash(user.password,password)):
            return None
        else:
            return user
    
    @staticmethod
    def get_user_role(user):
        user = User.query.filter_by(email=user.email).first()
        return user.role_id
    