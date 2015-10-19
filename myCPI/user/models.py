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

class UserEntry(Model):
    __tablename__ = 'userEntry'
    #Primary Key - needs to be autoincrementing
    entryID = Column(db.Integer, primary_key=True)
    date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    cpi_u = Column(db.Integer, nullable=True)

    def __repr__(self):
        return '{entryID}'.format(entryID=self.entryID)

class UserComponent(Model):
    __tablename__ = 'userComponent'
    #Primary Key
    component = Column(db.String(50), primary_key=True)
    #Primary Key, Foreign Key
    entryID = Column(db.Integer, db.ForeignKey('userEntry.entryID'),primary_key=True)
    index = Column(db.Integer, nullable=False)
    weight = Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<UserComponent({component})>'.format(component=self.component)

class ComponentCPI(Model):
    __tablename__ = 'componentCPI'
    #Primary Key
    component = Column(db.String(80), primary_key = True)
    #Primary key
    year = Column(db.Integer, primary_key = True)
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

    def __repr__(self):
        return '<ComponentCPI({component})>'.format(component=self.component)

class ComponentAge(Model):
   __tablename__ = 'componentAge'
   component = Column(db.String(80), primary_key = True)
   year = Column(db.Integer, primary_key = True)
   all_units = Column(db.Integer, nullable=True)
   under_25 = Column(db.Integer, nullable=True)
   age_25_to_34 = Column(db.Integer, nullable=True)
   age_35_to_44 = Column(db.Integer, nullable=True)
   age_45_to_54 = Column(db.Integer, nullable=True)
   age_55_to_64 = Column(db.Integer, nullable=True)
   age_65_to_older = Column(db.Integer, nullable=True)
   age_65_to_74 = Column(db.Integer, nullable=True)
   age_75_to_older = Column(db.Integer, nullable=True)

   def __repr__(self):
        return '<ComponentAge({component})>'.format(component=self.component)

   def __getitem__(self, key):
        return self.__dict__.__getitem__(key)        

class ComponentIncome(Model):
   __tablename__ = 'componentIncome'
   component = Column(db.String(80), primary_key = True)
   year = Column(db.Integer, primary_key = True)
   all_units = Column(db.Integer, nullable=True)
   lowest = Column(db.Integer, nullable=True)
   second = Column(db.Integer, nullable=True)
   third = Column(db.Integer, nullable=True)
   fourth = Column(db.Integer, nullable=True)
   fifth = Column(db.Integer, nullable=True)
   sixth = Column(db.Integer, nullable=True)
   seventh = Column(db.Integer, nullable=True)
   eighth = Column(db.Integer, nullable=True)
   ninth = Column(db.Integer, nullable=True)
   highest = Column(db.Integer, nullable=True)

   def __repr__(self):
        return '<ComponentIncome({component})>'.format(component=self.component)

   def __getitem__(self, key):
        return self.__dict__.__getitem__(key)


class ComponentRegions(Model):
   __tablename__ = 'componentRegions'
   component = Column(db.String(80), primary_key = True)
   year = Column(db.Integer, primary_key = True)
   all_units = Column(db.Integer, nullable=True)
   northeast = Column(db.Integer, nullable=True)
   midwest = Column(db.Integer, nullable=True)
   south = Column(db.Integer, nullable=True)
   west = Column(db.Integer, nullable=True)

   def __repr__(self):
        return '<ComponentRegions({component})>'.format(component=self.component)
    
   def __getitem__(self, key):
        return self.__dict__.__getitem__(key)


class ComponentEdu(Model):
   __tablename__ = 'componentEdu'
   component = Column(db.String(80), primary_key = True)
   year = Column(db.Integer, primary_key = True)
   total_less_than_graduate = Column(db.Integer, nullable=True)
   less_than_high_school = Column(db.Integer, nullable=True)
   high_school_grad = Column(db.Integer, nullable=True)
   assoc_degree = Column(db.Integer, nullable=True)
   total_college_grad = Column(db.Integer, nullable=True)
   bachelor_degree = Column(db.Integer, nullable=True)
   masters_degree = Column(db.Integer, nullable=True)

   def __repr__(self):
        return '<ComponentEdu({component})>'.format(component=self.component)

   def __getitem__(self, key):
        return self.__dict__.__getitem__(key)


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
