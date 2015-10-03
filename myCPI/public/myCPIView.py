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
    avg_share_data = {'None': None}
    if request.method == "POST":
        if form.validate_on_submit():
	    #create new entry in userEntry table for new values
            entryid = create_new_entry()
            avg_share_data = plot_avg_shares()
            #get form values 
            usercomp_indexes = {'food':form.food_share.data,'housing':form.housing_share.data,\
              'apparel':form.apparel_share.data,'education':form.edu_share.data,\
              'transportation':form.transportation_share.data,'medical_care':form.medical_share.data,\
              'recreation':form.recreation_share.data,'other':form.other_share.data}
            
            budget_sum = sum(usercomp_indexes.values())
            
            index_weights = {'food':usercomp_indexes['food']/budget_sum,'housing':usercomp_indexes['housing']/budget_sum,\
              'apparel':usercomp_indexes['apparel']/budget_sum,'education':usercomp_indexes['education']/budget_sum,\
              'transportation':usercomp_indexes['transportation']/budget_sum,'medical_care':usercomp_indexes['medical_care']/budget_sum,\
              'recreation':usercomp_indexes['recreation']/budget_sum,'other':usercomp_indexes['other']/budget_sum}
            
            my_cpi = compute_cpi(form,entryid,usercomp_indexes,index_weights)
            insert_user_values(usercomp_indexes,entryid,index_weights,my_cpi)
            share_data = plot_shares(form,index_weights)
        else:
            my_cpi = None
    elif request.method == "GET":
        my_cpi = None
    return render_template("public/mycpi.html", form=form, my_cpi=my_cpi, share_data=share_data, avg_share_data=avg_share_data)

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
    
def plot_shares(form, index_weights,chartID='chartID', chart_type='pie', chart_height=500):
    budget_shares = {}
    budget_shares['title'] = {"text": "Visualization of budget shares"}
    budget_shares['series'] = json.dumps([{'name': "Budget Share",\
            'colorByPoint': True,\
            'data':[\
                {"name":"Food/Beverage", "y": round(100*index_weights['food'], 2)},\
                {"name":"Housing", "y": round(100*index_weights['housing'], 2)},\
                {"name":"Apparel", "y": round(100*index_weights['apparel'], 2)},\
                {"name":"Transportation", "y": round(100*index_weights['transportation'], 2)},\
                {"name":"Medical Care", "y": round(100*index_weights['medical_care'], 2)},\
                {"name":"Recreation", "y": round(100*index_weights['recreation'], 2)},\
                {"name":"Education", "y": round(100*index_weights['education'], 2)},\
                {"name":"Other Services", "y": round(100*index_weights['other'], 2)}]}])
    budget_shares['page_type'] = "graph"
    budget_shares['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height}

    return budget_shares 
    
def plot_avg_shares(chartID='chartID1', chart_type='pie', chart_height=500):
    avg_budget_shares = {}
    avg_budget_shares['title'] = {"text": "Visualization of average budget shares"}
    avg_budget_shares['series'] = json.dumps([{'name': "Average Budget Share",\
            'colorByPoint': True,\
            'data':[\
                {"name":"Food/Beverage", "y":10},\
                {"name":"Housing", "y": 15},\
                {"name":"Apparel", "y": 20},\
                {"name":"Transportation", "y": 20},\
                {"name":"Medical Care", "y": 10},\
                {"name":"Recreation", "y": 10},\
                {"name":"Education", "y": 10},\
                {"name":"Other Services", "y": 5}]}])
    avg_budget_shares['page_type'] = "graph"
    avg_budget_shares['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    
    return avg_budget_shares      
@blueprint.route("/about/")
def about():
    form = BudgetShareForm(request.form)
    return render_template("public/about.html", form=form)
