# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import FloatField,TextField
from wtforms.validators import DataRequired


class BudgetShareForm(Form):
    food_share = FloatField('Food/Beverage', validators=[DataRequired()])
    housing_share = FloatField('Housing', validators=[DataRequired()])
    apparel_share = FloatField('Apparel', validators=[DataRequired()])
    transportation_share = FloatField('Transportation', validators=[DataRequired()])
    medical_share = FloatField('Medical Care', validators=[DataRequired()])
    recreation_share = FloatField('Recreation', validators=[DataRequired()])
    edu_share = FloatField('Education', validators=[DataRequired()])
    other_share = FloatField('Other Services', validators=[DataRequired()])
    
    my_cpi = FloatField("My Inflation (percent increase from 1982)")
    avg_cpi = TextField("Average Inflation")

    def __init__(self, *args, **kwargs):
        super(BudgetShareForm, self).__init__(*args, **kwargs)
        self.sum_error = False

    
    def validate(self):
        initial_validation = super(BudgetShareForm, self).validate()
        if not initial_validation:
            return False
         
        #if sum([self.food_share.data, 
        #self.housing_share.data, 
        #self.apparel_share.data, 
        #self.transportation_share.data, 
        #self.medical_share.data, 
        #self.recreation_share.data, 
        #self.edu_share.data, 
        #self.other_share.data]) != 1.0:
        #    self.sum_error = True
        #    return False
            
        return True
