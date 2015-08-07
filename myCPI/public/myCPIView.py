# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from myCPI.public.myCPIForms import BudgetShareForm

from myCPI.utils import flash_errors
from flask import flash


blueprint = Blueprint('mycpi', __name__, static_folder="../static")


@blueprint.route("/mycpi", methods=["GET", "POST"])
def enterBudgetShare():
    form = BudgetShareForm(request.form)
    sum_error = None
    if request.method == "POST":
        if form.validate_on_submit():
            my_cpi = compute_cpi(form)
            sum_error = None
        else:
            if form.sum_error:
                sum_error = "Budget shares don't sum to 1.0. Please enter inputs for each category as a share of your total budget'"
            my_cpi = None
    elif request.method == "GET":
        my_cpi = None
        sum_error = None  
    return render_template("public/mycpi.html", form=form, my_cpi=my_cpi, sum_error=sum_error)
    
def compute_cpi(form):
    component_indexes = {'food':246.245,\
        'housing':238.568,\
        'apparel': 124.954,\
        'edu': 137.425,\
        'transport': 208.012,\
        'medical_care': 446.271,\
        'recreation': 116.395,\
        'other': 415.022}
    budget_sum = (form.food_share.data+form.housing_share.data+form.apparel_share.data+form.edu_share.data+ \
        form.transportation_share.data+form.medical_share.data+form.recreation_share.data+form.other_share.data)
    wgted_sum = (form.food_share.data/budget_sum * component_indexes['food']/100 + \
        form.housing_share.data/budget_sum * component_indexes['housing']/100 + \
        form.apparel_share.data/budget_sum * component_indexes['apparel']/100 + \
        form.edu_share.data/budget_sum * component_indexes['edu']/100 + \
        form.transportation_share.data/budget_sum * component_indexes['transport']/100 + \
        form.medical_share.data/budget_sum * component_indexes['medical_care']/100 + \
        form.recreation_share.data/budget_sum * component_indexes['recreation']/100 + \
        form.other_share.data/budget_sum * component_indexes['other']/100)
    inflation = wgted_sum - 1
    inflation *= 100
    return round(inflation,3)

    
@blueprint.route("/about/")
def about():
    form = BudgetShareForm(request.form)
    return render_template("public/about.html", form=form)
