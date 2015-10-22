# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from myCPI.public.myCPIForms import BudgetShareForm, choices
from myCPI.database import db
from myCPI.user.models import ComponentCPI,UserEntry,UserComponent,ComponentAge,ComponentIncome,ComponentRegions,ComponentEdu
import json,datetime
from sqlalchemy import and_
import pdb
blueprint = Blueprint('mycpi', __name__, static_folder="../static")

table_lookup = {'ComponentRegions': ComponentRegions,\
    'ComponentAge': ComponentAge,\
    'ComponentEdu': ComponentEdu,\
    'ComponentIncome': ComponentIncome}

    
@blueprint.route("/mycpi", methods=["GET", "POST"])
def enterBudgetShare():
    form = BudgetShareForm(request.form)
    share_data = {'None': None}
    cpi_data = {'None': None}
    national_cpi = getNationalCPI()
    print national_cpi    
    
    if request.method == "POST":
        if form.validate_on_submit():
            #create new entry in userEntry table for new values
            entryid = create_new_entry()

            # get component names
            component_names = {'food': form.food_share.label.text, 'housing': form.housing_share.label.text, 'apparel': form.apparel_share.label.text, 'education': form.edu_share.label.text, 
            'transportation': form.transportation_share.label.text, 
            'medical_care': form.medical_share.label.text, 'recreation': form.recreation_share.label.text, 'other': form.other_share.label.text}
            # get demographic names
            demo_names = {'age': form.age_group.label.text, 'edu': form.edu_level.label.text, 'income': form.income_group.label.text, 'rgn': form.rgn_residence.label.text}
            
            # get user info
            user_budget = get_user_budget(form)
            user_demo = get_user_demographics(form)

            # get national average shares
            national_weights = get_national_weights()
            # get user's budget shares
            user_weights = get_user_weights(user_budget)
            # get shares by age group
            age_weights = get_weights('Age', form.age_group.data)
            # get shares by education level
            edu_weights = get_weights('Edu', form.edu_level.data)
            # get shares by income level
            income_weights = get_weights('Income', form.income_group.data)
            # get shares by region of residence
            rgn_weights = get_weights('Regions', form.rgn_residence.data)
            
            # get component indexes
            component_indexes = get_component_indexes()
            # calculate user's customized cpi
            my_cpi = compute_cpi(component_indexes,user_weights)
            # calculate the national cpi
            # national_cpi = compute_cpi(component_indexes, national_weights)
            # calculate cpi for user's age group
            age_cpi = compute_cpi(component_indexes, age_weights)
            # calculate cpi for user's education level
            edu_cpi = compute_cpi(component_indexes, edu_weights)
            # calculate cpi for user's income group
            income_cpi = compute_cpi(component_indexes, income_weights)
            # calculate cpi for user's region of residence
            rgn_cpi = compute_cpi(component_indexes, rgn_weights)

            
            insert_user_values(user_budget,entryid,user_weights,my_cpi)
            # share_data = plot_shares(component_names, national_weights, user_weights)
            share_data = plot_vis(component_names, national_weights, user_weights, age_weights, edu_weights, income_weights, rgn_weights)
            cpi_data = plot_cpi(national_cpi, my_cpi, age_cpi, edu_cpi, income_cpi, rgn_cpi)
            print cpi_data
        else:
            my_cpi = None
    elif request.method == "GET":
        my_cpi = None
        
    return render_template("public/mycpi.html", form=form, national_cpi=national_cpi, my_cpi=my_cpi, share_data=share_data, cpi_data=cpi_data )

def get_user_weights(user_budget):
    # calculate budget sum
    budget_sum = float(sum(user_budget.values()))    
    # calculate budget shares of each component
    user_weights = {'food':user_budget['food']/budget_sum,\
                    'housing':user_budget['housing']/budget_sum,\
                    'apparel':user_budget['apparel']/budget_sum,
                    'education':user_budget['education']/budget_sum,\
                    'transportation':user_budget['transportation']/budget_sum,
                    'medical_care':user_budget['medical_care']/budget_sum,\
                    'recreation':user_budget['recreation']/budget_sum,\
                    'other':user_budget['other']/budget_sum}

    return user_weights

    
def get_national_weights():
    #national_component_weights = {'apparel': 0.03338629778, 'education': 0.02310496308, 'food': 0.1350032713, 'housing': 0.332703991, 'medical_care': 0.1872324516, 'other': 0.0679876624,\
    #    'recreation': 0.05099542013, 'transportation': 0.1696046359}    
    national_component_weights = {}
    
    national_compo = ComponentCPI.query.with_entities(ComponentCPI.component,ComponentCPI.weight)\
    .filter(and_(ComponentCPI.year == 2014,ComponentCPI.component != 'All items')).all()
    
    for row in national_compo:
        # the weights for each component at the national level (row.weight) are parts of a 100.
        national_component_weights.update({row.component.lower().replace(" ","_"):row.weight})
    
    national_budget_sum = float(sum(national_component_weights.values()))
    # calculate budget shares of each component
    national_weights = {'food':national_component_weights['food']/national_budget_sum,\
        'housing':national_component_weights['housing']/national_budget_sum,\
        'apparel':national_component_weights['apparel']/national_budget_sum,\
        'education':national_component_weights['education']/national_budget_sum,\
        'transportation':national_component_weights['transportation']/national_budget_sum,\
        'medical_care':national_component_weights['medical_care']/national_budget_sum,\
        'recreation':national_component_weights['recreation']/national_budget_sum,\
        'other':national_component_weights['other']/national_budget_sum}
    
    return national_weights


def get_user_budget(form):
    #get form values 
    return {'food':int(round(form.food_share.data)),
            'housing':int(round(form.housing_share.data)),\
            'apparel':int(round(form.apparel_share.data)),
            'education':int(round(form.edu_share.data)),\
            'transportation':int(round(form.transportation_share.data)),
            'medical_care':int(round(form.medical_share.data)),\
            'recreation':int(round(form.recreation_share.data)),
            'other':int(round(form.other_share.data))}


def get_user_demographics(form):
    return {'age': choices['Age'][form.age_group.data]['choice'],\
            'edu': choices['Edu'][form.edu_level.data]['choice'],\
            'income': choices['Income'][form.income_group.data]['choice'],\
            'rgn': choices['Regions'][form.rgn_residence.data]['choice']}
    

def get_weights(component, index):
    weights = {}
    tableObj = table_lookup.get('Component' + component)
    col_name = choices[component][index]['col']
    for row in tableObj.query.all():
        # print row.component, row[col_name]
        weights[row.component.strip().lower().replace(" ","_")] = row[col_name]
    return weights

def create_new_entry():
    #create new entry in userEntry table for new values
    user_entry = UserEntry.create(date=datetime.datetime.now(),cpi_u="")
    entryid = getattr(user_entry,"entryID")
    
    return entryid

def getNationalCPI():
    #get national cpi value to display on the form
    results = ComponentCPI.query.with_entities(ComponentCPI.cpi_u_annual)\
    .filter(and_(ComponentCPI.year == 2014,ComponentCPI.component == 'All items')).one()
    national_cpi = results[0];

    return national_cpi[0][0]


def get_component_indexes():
    component_indexes = {}

    #get indexes from componentCPI table - cpi_u_annual for year 2014 for now
    compo_indexes = ComponentCPI.query.with_entities(ComponentCPI.component,ComponentCPI.cpi_u_annual)\
    .filter(and_(ComponentCPI.year == 2014,ComponentCPI.component != 'All items')).all()
    
    for row in compo_indexes:
        component_indexes.update({row.component.strip().lower().replace(" ","_"):row.cpi_u_annual})
    
    return component_indexes


def compute_cpi(component_indexes, weights):
    
    ref_indexes = {'food':100,\
        'housing':100,\
        'apparel': 100,\
        'education': 100,\
        'transportation': 100,\
        'medical_care': 100,\
        'recreation': 100,\
        'other': 100}

    wgted_sum = (\
        weights['food'] * component_indexes['food']/ref_indexes['food'] +\
        weights['housing'] * component_indexes['housing']/ref_indexes['housing'] +\
        weights['apparel'] * component_indexes['apparel']/ref_indexes['apparel'] +\
        weights['education'] * component_indexes['education']/ref_indexes['education'] +\
        weights['transportation'] * component_indexes['transportation']/ref_indexes['transportation'] +\
        weights['medical_care'] * component_indexes['medical_care']/ref_indexes['medical_care'] +\
        weights['recreation'] * component_indexes['recreation']/ref_indexes['recreation'] +\
        weights['other'] * component_indexes['other']/ref_indexes['other'])
    
    inflation = wgted_sum * 100
    mycpi = round(inflation,3)
    
    return mycpi

def insert_user_values(usercomp_indexes,entryid,index_weights,my_cpi):
    #for all components, insert component,index,weight    
    for key,value in usercomp_indexes.iteritems():
          usercomp = UserComponent.create(component=key,entryID=entryid,index=value,weight=index_weights[key])
    
    #then insert cpi_u into userEntry for id
    user_entry = UserEntry.query.filter(UserEntry.entryID == entryid).first()
    stmt = user_entry.update(cpi_u = my_cpi)


def plot_vis(component_names, national_weights, user_weights, age_weights, edu_weights, income_weights, rgn_weights, chartID='chart-stacked-bar', chart_type='column', chart_height=500):
    data = {}
    components = sorted(component_names.keys())

    data['title'] = {"text": "Comparison of Budget shares"}
    data['xAxis'] = {"categories": ["National", "You", "Age Group", "Education Level", "Income Level", "Region Of Residence"  ]}
    data['yAxis'] = {"min": 0, "title": {"text": "Component shares"}}
    data['legend'] = {"reversed": True}
    data['plotOptions'] = {"series": {"stacking": "normal"}}
    data['page_type'] = "graph"

    d = []
    for name in components:
        d.append({"name": component_names[name], "data": [national_weights[name], user_weights[name], age_weights[name], edu_weights[name], income_weights[name], rgn_weights[name]]})
    data["series"] = json.dumps(d)
    data['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height, "xAxis": {"categories": [ component_names[name] for name in components]}, "yAxis": {"min": 0, "title": {"text": "Component shares"}}}
    
    return data    


def plot_cpi(national_cpi, my_cpi, age_cpi, edu_cpi, income_cpi, rgn_cpi, chartID='chart-line', chart_type='line', chart_height=500):
    data = {}
    data['title'] = {"text": "Comparison of Price Indexes"}
    data['xAxis'] = {"categories": ["National", "You", "Age Group", "Education Level", "Income Level", "Region Of Residence"  ]}
    data['yAxis'] = {"min": 150, "title": {"text": "Component Price Index"}}
    data['series'] = json.dumps([{"name": "Component Index", "data":[national_cpi, my_cpi, age_cpi, edu_cpi, income_cpi, rgn_cpi]}])
    data['page_type'] = "graph"
    data['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    return data
    
def plot_shares(component_names, national_weights, user_weights, chartID='chart-stacked-bar-1', chart_type='column', chart_height=500):
    data = {}
    components = sorted(component_names.keys())

    data['title'] = {"text": "Comparison of User shares by component with the national average"}
    data['xAxis'] = {"categories": [ component_names[name] for name in components]}
    data['yAxis'] = {"min": 0, "title": {"text": "Component shares"}}
    data["legend"] = {"reversed": True}
    data["plotOptions"] = {"series": {"stacking": "normal"}}
    
    data["series"] = json.dumps([{"name": 'Your budget share', "data": [round(user_weights[name],3) for name in components]}, \
        {"name": "Average national budget share", "data": [ round(national_weights[name], 3) for name in components]}])
    data['page_type'] = "graph"
    data['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height, "xAxis": {"categories": [ component_names[name] for name in components]}, "yAxis": {"min": 0, "title": {"text": "Component shares"}}}
    
    return data
    
    
@blueprint.route("/about/")
def about():
    form = BudgetShareForm(request.form)
    return render_template("public/about.html", form=form)
