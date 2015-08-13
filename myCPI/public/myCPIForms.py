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
    
    my_cpi = FloatField("My Personal Inflation (Base=100)")
    avg_cpi = TextField("Average National Inflation")

    def __init__(self, *args, **kwargs):
        super(BudgetShareForm, self).__init__(*args, **kwargs)
    
    def validate(self):
        initial_validation = super(BudgetShareForm, self).validate()
        if not initial_validation:
            return False
            
        return True
