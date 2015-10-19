# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import FloatField,TextField, SelectField
from wtforms.validators import DataRequired

choices = \
    {
        'Regions':\
        {
            '0': {'col': 'northeast', 'choice': ('0', 'North East')},\
            '1': {'col': 'midwest', 'choice': ('1', 'Mid West')},\
            '2':{'col': 'south', 'choice': ('2', 'South')},\
            '3': {'col': 'west', 'choice': ('3', 'West')}
        },
        'Age':\
        {
            '0': {'col': 'under_25', 'choice': ('0', '<25')},
            '1': {'col': 'age_25_to_34', 'choice': ('1', '25-34')},
            '2': {'col': 'age_35_to_44', 'choice': ('2', '35-44')},
            '3': {'col': 'age_45_to_54', 'choice': ('3', '45-54')},
            '4': {'col': 'age_55_to_64', 'choice': ('4', '55-64')},
            '5': {'col': 'age_65_to_74', 'choice': ('5', '65-74')},
            '6': {'col': 'age_75_to_older', 'choice': ('6', '>=75')}
        },
        'Edu':\
        {
            '0': {'col': 'less_than_high_school', 'choice': ('0', 'Less than High School')},
            '1': {'col': 'high_school_grad', 'choice': ('1', 'High School graduate')},
            '2': {'col': 'assoc_degree', 'choice': ('2', 'Associate Degree')},
            '3': {'col': 'bachelor_degree', 'choice': ('3','Bachelor Degree')},
            '4': {'col': 'masters_degree', 'choice': ('4', 'Masters Degree or higher')}
        },
        'Income':\
        {
            '0': {'col': 'lowest', 'choice': ('0', 'lowest')},
            '1': {'col': 'second', 'choice': ('1', 'second')},
            '2': {'col': 'third', 'choice': ('2', 'third')},
            '3': {'col': 'fourth', 'choice': ('3', 'fourth')},
            '4': {'col': 'fifth', 'choice': ('4', 'fifth')},
            '5': {'col': 'sixth', 'choice': ('5', 'sixth')},
            '6': {'col': 'seventh', 'choice': ('6', 'seventh')},
            '7': {'col': 'eigth', 'choice': ('7', 'eigth')},
            '8': {'col': 'ninth', 'choice': ('8', 'ninth')},
            '9': {'col': 'highest', 'choice': ('9', 'highest')}
        }
    }


class BudgetShareForm(Form):
    food_share = FloatField('Food/Beverage', validators=[DataRequired()])
    housing_share = FloatField('Housing', validators=[DataRequired()])
    apparel_share = FloatField('Apparel', validators=[DataRequired()])
    transportation_share = FloatField('Transportation', validators=[DataRequired()])
    medical_share = FloatField('Medical Care', validators=[DataRequired()])
    recreation_share = FloatField('Recreation', validators=[DataRequired()])
    edu_share = FloatField('Education', validators=[DataRequired()])
    other_share = FloatField('Other Services', validators=[DataRequired()])

    rgn_residence = SelectField('Region of Residence', choices=[d['choice'] for d in sorted(choices['Regions'].values())])
    age_group = SelectField("Age Group", choices=[d['choice'] for d in sorted(choices['Age'].values())], validators=[DataRequired()])
    income_group = SelectField("Income Range", choices=[d['choice'] for d in sorted(choices['Income'].values())], validators=[DataRequired()])
    edu_level = SelectField("Educational Qualification", choices=[d['choice'] for d in sorted(choices['Edu'].values())], validators=[DataRequired()])
    
    my_cpi = FloatField("My Personal Inflation (Base=100)")
    avg_cpi = TextField("Average National Inflation")

    def __init__(self, *args, **kwargs):
        super(BudgetShareForm, self).__init__(*args, **kwargs)
    
    def validate(self):
        initial_validation = super(BudgetShareForm, self).validate()
        if not initial_validation:
            return False
            
        return True
