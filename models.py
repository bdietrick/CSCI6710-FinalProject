# from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
import util
import sqlalchemy as db
#from sqlalchemy import create_engine, select, insert, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# Base = declarative_base()
engine = db.create_engine('sqlite:///GardenExchange.db', connect_args={'check_same_thread': False}, echo=False)
connection = engine.connect()
metadata = db.MetaData()

# engine.execute('CREATE DATABASE GardenExchange;')
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# Base.metadata.create_all(engine)

login = LoginManager()
#db = SQLAlchemy()

plants = db.Table('plants', metadata,
                  db.Column('id', db.Integer()),
                  db.Column('name', db.String(64)),
                  db.Column('description', db.Column(db.String(256))),
                  db.Column('image', db.Column(db.String(64))))

users = db.Table('users', metadata,
                 db.Column('id', db.Integer(),primary_key=True),
                 db.Column('email', db.String(128), unique=True),
                 db.Column('username', db.String(128)),
                 db.Column('password_hash', db.String(256)))

metadata.create_all(engine)

# class Plant(Base):
#     __tablename__ = 'plants'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     description = db.Column(db.String(256))
#     image = db.Column(db.String(64))
#
#     def __repr__(self):
#         return '<Item %r' % self.name


# class UserModel(UserMixin, Base):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(80), unique=True)
#     username = db.Column(db.String(100))
#     password_hash = db.Column(db.String())
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return session.query(UserModel).get(int(id))