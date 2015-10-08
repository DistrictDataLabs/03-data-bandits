# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from myCPI.public.myCPIForms import BudgetShareForm
from myCPI.database import db
from myCPI.user.models import ComponentCPI,UserEntry,UserComponent
import json,datetime
from sqlalchemy import and_

blueprint = Blueprint('mycpi', __name__, static_folder="../static")


@blueprint.route("/mycpi", methods=["GET", "POST"])
def enterBudgetShare():
    form = BudgetShareForm(request.form)
    share_data = {'None': None}

    if request.method == "POST":
        if form.validate_on_submit():
            #create new entry in userEntry table for new values
            entryid = create_new_entry()
            #get form values 
            usercomp_indexes = {'food':int(round(form.food_share.data)),'housing':int(round(form.housing_share.data)),\
              'apparel':int(round(form.apparel_share.data)),'education':int(round(form.edu_share.data)),\
              'transportation':int(round(form.transportation_share.data)),'medical_care':int(round(form.medical_share.data)),\
              'recreation':int(round(form.recreation_share.data)),'other':int(round(form.other_share.data))}
            # get component names
            component_names = {'food': form.food_share.label.text, 'housing': form.housing_share.label.text, 'apparel': form.apparel_share.label.text, 'education': form.edu_share.label.text, 
            'transportation': form.transportation_share.label.text, 
            'medical_care': form.medical_share.label.text, 'recreation': form.recreation_share.label.text, 'other': form.other_share.label.text}
            # calculate budget sum
            budget_sum = float(sum(usercomp_indexes.values()))
            # calculate budget shares of each component
            index_weights = {'food':usercomp_indexes['food']/budget_sum,'housing':usercomp_indexes['housing']/budget_sum,\
              'apparel':usercomp_indexes['apparel']/budget_sum,'education':usercomp_indexes['education']/budget_sum,\
              'transportation':usercomp_indexes['transportation']/budget_sum,'medical_care':usercomp_indexes['medical_care']/budget_sum,\
              'recreation':usercomp_indexes['recreation']/budget_sum,'other':usercomp_indexes['other']/budget_sum}
            # calculate user's customized cpi
            my_cpi = compute_cpi(form,entryid,usercomp_indexes,index_weights)
            insert_user_values(usercomp_indexes,entryid,index_weights,my_cpi)
            share_data = plot_shares(form, component_names, index_weights)
        else:
            my_cpi = None
    elif request.method == "GET":
        my_cpi = None
        
    return render_template("public/mycpi.html", form=form, my_cpi=my_cpi, share_data=share_data)

def create_new_entry():
    #create new entry in userEntry table for new values
    user_entry = UserEntry.create(date=datetime.datetime.now(),cpi_u="")
    entryid = getattr(user_entry,"entryID")
    
    return entryid
    
def compute_cpi(form,entryid,usercomp_indexes,index_weights):
    component_indexes = {}

    #get indexes from componentCPI table - cpi_u_annual for year 2014 for now
    compo_indexes = ComponentCPI.query.with_entities(ComponentCPI.component,ComponentCPI.cpi_u_annual)\
    .filter(and_(ComponentCPI.year == 2014,ComponentCPI.component != 'All items')).all()
    print compo_indexes
    for row in compo_indexes:
        component_indexes.update({row.component.lower().replace(" ","_"):row.cpi_u_annual})
    
    print component_indexes

    ref_indexes = {'food':100,\
        'housing':100,\
        'apparel': 100,\
        'education': 100,\
        'transportation': 100,\
        'medical_care': 100,\
        'recreation': 100,\
        'other': 100}
    
    wgted_sum = (index_weights['food'] * component_indexes['food']/ref_indexes['food'] +\
        index_weights['housing'] * component_indexes['housing']/ref_indexes['housing'] +\
        index_weights['apparel'] * component_indexes['apparel']/ref_indexes['apparel'] +\
        index_weights['education'] * component_indexes['education']/ref_indexes['education'] +\
        index_weights['transportation'] * component_indexes['transportation']/ref_indexes['transportation'] +\
        index_weights['medical_care'] * component_indexes['medical_care']/ref_indexes['medical_care'] +\
        index_weights['recreation'] * component_indexes['recreation']/ref_indexes['recreation'] +\
        index_weights['other'] * component_indexes['other']/ref_indexes['other'])
    
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

def plot_shares(form, component_names, index_weights, chartID='chart-stacked-bar', chart_type='column', chart_height=500):
    data = {}
    components = sorted(component_names.keys())
    national_component_weights = {'apparel': 0.03338629778, 'education': 0.02310496308, 'food': 0.1350032713, 'housing': 0.332703991, 'medical_care': 0.1872324516, 'other': 0.0679876624,\
        'recreation': 0.05099542013, 'transportation': 0.1696046359}
    data['title'] = {"text": "Comparison of User shares by component with the national average"}
    
    data['xAxis'] = {"categories": [ component_names[name] for name in components]}
    data['yAxis'] = {"min": 0, "title": {"text": "Component shares"}}
    data["legend"] = {"reversed": True}
    data["plotOptions"] = {"series": {"stacking": "normal"}}
    
    data["series"] = json.dumps([{"name": 'Your budget share', "data": [round(index_weights[name],3) for name in components]}, \
        {"name": "Average national budget share", "data": [ round(national_component_weights[name], 3) for name in components]}])
    data['page_type'] = "graph"
    data['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height, "xAxis": {"categories": [ component_names[name] for name in components]}, "yAxis": {"min": 0, "title": {"text": "Component shares"}}}
    
    return data
    
    
@blueprint.route("/about/")
def about():
    form = BudgetShareForm(request.form)
    return render_template("public/about.html", form=form)
