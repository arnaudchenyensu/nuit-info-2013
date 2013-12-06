from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(70))
    entries = relationship('Entry', backref='user', lazy='dynamic')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    
    def __repr__(self):
        return '<User %r>' % (self.username)


    def is_active(self):
        return True


    def get_id(self):
        return unicode(self.id)



class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True)
    text = Column(String(120))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<User %r>' % (self.username)