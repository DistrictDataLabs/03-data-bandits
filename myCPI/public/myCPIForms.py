# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import FloatField,TextField, SelectField
from wtforms.validators import DataRequired

choices = \
    {
        'Regions':\
        {
            '0': {'col': 'northeast', 'choice': ('0', 'Northeast')},\
            '1': {'col': 'midwest', 'choice': ('1', 'Midwest')},\
            '2':{'col': 'south', 'choice': ('2', 'South')},\
            '3': {'col': 'west', 'choice': ('3', 'West')}
        },
        'Age':\
        {
            '0': {'col': 'under_25', 'choice': ('0', 'Under 25')},
            '1': {'col': 'age_25_to_34', 'choice': ('1', '25-34')},
            '2': {'col': 'age_35_to_44', 'choice': ('2', '35-44')},
            '3': {'col': 'age_45_to_54', 'choice': ('3', '45-54')},
            '4': {'col': 'age_55_to_64', 'choice': ('4', '55-64')},
            '5': {'col': 'age_65_to_74', 'choice': ('5', '65-74')},
            '6': {'col': 'age_75_to_older', 'choice': ('6', '75 or Older')}
        },
        'Edu':\
        {
            '0': {'col': 'less_than_high_school', 'choice': ('0', 'Less than High School')},
            '1': {'col': 'high_school_grad', 'choice': ('1', 'High School Graduate')},
            '2': {'col': 'assoc_degree', 'choice': ('2', 'Associate Degree')},
            '3': {'col': 'bachelor_degree', 'choice': ('3','Bachelor Degree')},
            '4': {'col': 'masters_degree', 'choice': ('4', 'Masters Degree or Higher')}
        },
        'Income':\
        {
            '0': {'col': 'less_than_five', 'choice': ('0', 'Less than $5,000')},
            '1': {'col': 'five_to_ten', 'choice': ('1', '$5000 to $9,999')},
            '2': {'col': 'ten_to_fifteen', 'choice': ('2', '$10,000 to $14,999')},
            '3': {'col': 'fifteen_to_twenty', 'choice': ('3', '$15,000 to $19,999')},
            '4': {'col': 'twenty_to_thirty', 'choice': ('4', '$20,000 to $29,999')},
            '5': {'col': 'thirty_to_fourty', 'choice': ('5', '$30,000 to $39,999')},
            '6': {'col': 'fourty_to_fifty', 'choice': ('6', '$40,000 to $49,999')},
            '7': {'col': 'fifty_to_seventy', 'choice': ('7', '$50,000 to $69,999')},
            '8': {'col': 'seventy_or_more', 'choice': ('8', '$70,000 and more')},
        }
    }


class BudgetShareForm(Form):
    budget_form_title = TextField("Budgetary Expenses")
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
