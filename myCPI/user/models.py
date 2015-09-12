# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin

from myCPI.extensions import bcrypt
from myCPI.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

#need to store indexes.  Still have not figured out where to get that data and how to store! Take step back with cpi vs index values

class UserEntry(SurrogatePK, Model):
    __tablename__ = 'userEntry'
    #Primary Key
    #entryID
    date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    cpi_u = Column(db.Integer, nullable=True)

    def __init__(self,date,cpi_u):
        db.Model.__init__(self,date=date,cpi_u=cpi_u,**kwargs)

class UserComponent(SurrogatePK, Model):
    __tablename__ = 'userComponent'
    #Primary Key
    component = Column(db.String(50), nullable=False)
    #Primary Key, Foreign Key
    #entryID = 
    index = Column(db.Integer, nullable=False)
    weight = Column(db.Integer, nullable=False)
    
    def __init__(self,component,index,weight, **kwargs):
        db.Model___init__(self,component=component,index=index,weight=weight)

class ComponentCPI(SurrogatePK, Model):
    __tablename__ = 'componentCPI'
    #Primary Key
    component = Column(db.String(80), nullable=False)
    #Primary key
    year = Column(db.Integer, nullable=False)
    cpi_jan = Column(db.Integer, nullable=True)
    cpi_feb = Column(db.Integer, nullable=True)
    cpi_march = Column(db.Integer, nullable=True)
    cpi_april = Column(db.Integer, nullable=True)
    cpi_may = Column(db.Integer, nullable=True)
    cpi_june = Column(db.Integer, nullable=True)
    cpi_aug = Column(db.Integer, nullable=True)
    cpi_sept = Column(db.Integer, nullable=True)
    cpi_oct = Column(db.Integer, nullable=True)
    cpi_nov = Column(db.Integer, nullable=True)
    cpi_dec = Column(db.Integer, nullable=True)
    cpi_u_half1 = Column(db.Integer, nullable=True)
    cpi_u_half2 = Column(db.Integer, nullable=True)
    cpi_u_annual = Column(db.Integer, nullable=True)
    weight = Column(db.Integer, nullable=True)

    def __init__(self,component,year,cpi_jan,cpi_feb,cpi_march,cpi_april,cpi_may,cpi_june,cpi_aug,cpi_sept,cpi_oct,
        cpi_nov,cpi_dec,cpi_u_half1,cpi_u_half2,cpi_u_annual,weight, **kwargs):
		db.Model__init__(self,component=component,year=year,cpi_jan=cpi_jan,cpi_feb=cpi_feb,cpi_march=cpi_march,
		cpi_april=cpi_april,cpi_may=cpi_may,cpi_june=cpi_june,cpi_aug=cpi_aug,cpi_sept=cpi_sept,cpi_oct=cpi_oct,
                cpi_nov=cpi_nov,cpi_dec=cpi_dec,cpi_u_half1=cpi_u_half1,cpi_u_half2=cpi_u_annual,weight=weight, **kwargs) 

class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
