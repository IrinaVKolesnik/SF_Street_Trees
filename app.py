# Imports
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import os 
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, select, extract
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import label
import json 
app = Flask(__name__)


#################################################
# Database Setup
#################################################
dbfile = os.path.join('db', 'data.sqlite')
engine = create_engine(f"sqlite:///{dbfile}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#################################################
# Database Setup
#################################################
tree_table = Base.classes.trees

# Create our session (link) from Python to the DB
session = Session(engine)



@app.route("/")
def index():
    return render_template("indexDash.html")

@app.route("/alldata")
def all_data():
   
   result = engine.execute("SELECT * from trees")
   
   All_Data_Trees=[]
   for r in result:
    All_Data_Trees.append({"tree_id":r[0],"Address":r[1],"Care_Taker":r[2],"Latitude":r[3],"Legal_Status":r[4],"Longitude":r[5],"Plant_Date":r[6],"Site_Info":r[7],"Species":r[8],"Foliage":r[9]})
   return jsonify(All_Data_Trees)

#latitude, longitude, species, tree id, care taker for amy
#ree_dict["plant_date"]=tree_data.plant_date
@app.route("/map_data")
def map():
   result = engine.execute("SELECT * from trees")
   map_data=[]
   for r in result:
    map_data.append({"tree_id":r[0],"Address":r[1],"Care_Taker":r[2],"Latitude":r[3],"Longitude":r[5],"Species":r[8]})
   
        
   return jsonify(map_data)


@app.route('/tree/<id>')
def tree(id):
    tree_data=session.query(tree_table).filter(tree_table.tree_id==id).one() 
    tree_dict={}
    tree_dict["address"]=tree_data.address
    tree_dict["plant_date"]=tree_data.plant_date
    return jsonify(tree_dict)

@app.route('/care')
def CaretakerAll():
    care_data= session.query(tree_table.care_taker,
        label('count', func.count(tree_table.tree_id))).group_by(
            tree_table.care_taker).order_by(
                func.count(tree_table.tree_id).desc()).all()
    result = [{"caretakers" : [c[0] for c in care_data],
          "counts" : [c[1] for c in care_data]}]
    return jsonify(result)

'''the oldest tree'''
@app.route('/oldest')
def Oldest():
    tree_data=session.query(tree_table.plant_date, tree_table.species, tree_table.address, 
        func.min(func.ifnull(tree_table.plant_date, date(3000, 1, 1)))).filter(
            tree_table.plant_date>date(1800, 1, 1)).one() 
    tree_dict={}
    tree_dict["plant_date"]=tree_data.plant_date
    tree_dict["species"]=tree_data.species
    tree_dict["address"]=tree_data.address
    return jsonify(tree_dict)

'''The 10 most popular trees in SF'''
@app.route('/topspecies')
def TopSpecies():
    species_data = session.query(tree_table.species,
        label('count', func.count(tree_table.tree_id))).group_by(
            tree_table.species).order_by(
                func.count(tree_table.tree_id).desc()).limit(10).all()
    species_list = [{"names" : [c[0] for c in species_data], "counts" : [c[1] for c in species_data]}]
    return jsonify(species_list)
    
'''The 10 most popular trees on Property side (site_info, Sidewalk: Property side : Cutout)'''''''''''''''''
@app.route('/toponproperty')
def TopOnProperty():
    onProp_data = session.query(tree_table.species,
        label('count', func.count(tree_table.tree_id))).filter(
            tree_table.site_info=="Sidewalk: Property side : Cutout").group_by(
                tree_table.species).order_by(
                    func.count(tree_table.tree_id).desc()).limit(10).all()
    onProp_list = [{"names" : [c[0] for c in onProp_data], "counts": [c[1] for c in onProp_data]}]
    return jsonify(onProp_list)

'''The 10 most popular trees on Curb (site_info, Sidewalk: Curb side: Cutout)'''
@app.route('/toponcurb')
def TopOnCurb():
    onCurb_data = session.query(tree_table.species,
        label('count', func.count(tree_table.tree_id))).group_by(
            tree_table.site_info=="Sidewalk: Curb side : Cutout").group_by(
              tree_table.species).order_by(
                func.count(tree_table.tree_id).desc()).limit(10).all()
    onCurb_list = [{"names" : [c[0] for c in onCurb_data], "counts": [c[1] for c in onCurb_data]}]
    return jsonify(onCurb_list)

'''The 10 most popular deciduous trees'''
@app.route('/topdeciduous')
def TopDeciduous():
    topDeciduous_data = session.query(tree_table.species,
        label('count', func.count(tree_table.tree_id))).filter(
            tree_table.foliage=="deciduous").group_by(
                tree_table.species).order_by(
                    func.count(tree_table.tree_id).desc()).limit(10).all()
    topDeciduous_list = [{"names" : [c[0] for c in topDeciduous_data], "counts": [c[1] for c in topDeciduous_data]}]
    return jsonify(topDeciduous_list)  

'''The 10 most popular evergreen trees'''
@app.route('/topevergreen')
def TopEvergreen():
    topEvergreen_data = session.query(tree_table.species,
        label('count', func.count(tree_table.tree_id))).filter(
            tree_table.foliage=="evergreen").group_by(
                tree_table.species).order_by(
                    func.count(tree_table.tree_id).desc()).limit(10).all()
    topEvergreen_list = [{"names" : [c[0] for c in topEvergreen_data], "counts": [c[1] for c in topEvergreen_data]}]
    return jsonify(topEvergreen_list)
    
'''Variety of evergreens vs deciduous trees'''
@app.route('/topfoliagevariety')
def TopFoliageVariety():
    topVariety_data = session.query(tree_table.species).distinct().filter(
            tree_table.foliage=="evergreen").all()
    topVariety_list = []
    topVariety_dict = {}
    topVariety_dict["foliage"]="evergreen"
    topVariety_dict["species_count"]=len(topVariety_data)
    topVariety_list.append(topVariety_dict)

    topVariety_data = session.query(tree_table.species).distinct().filter(
            tree_table.foliage=="deciduous").all()
    topVariety_dict = {}
    topVariety_dict["foliage"]="deciduous"
    topVariety_dict["species_count"]=len(topVariety_data)
    topVariety_list.append(topVariety_dict)

    return jsonify(topVariety_list)

'''Amount of evergreens vs deciduous'''
@app.route('/foliage')
def FoliageAll():
    foliage_data= session.query(tree_table.foliage,
        label('count', func.count(tree_table.tree_id))).group_by(
            tree_table.foliage).order_by(
                func.count(tree_table.tree_id).desc()).all()
    result = [{"foliages" : [c[0] for c in foliage_data],
          "counts" : [c[1] for c in foliage_data]}]
    return jsonify(result)

'''Variety of all trees'''
@app.route('/allvariety')
def AllVariety():
    allVariety_data = session.query(tree_table.species).distinct().all()
    allVariety_list = []
    allVariety_dict = {}
    allVariety_dict["foliage"]="all"
    allVariety_dict["species_count"]=len(allVariety_data)
    allVariety_list.append(allVariety_dict)
    return jsonify(allVariety_list)

@app.route('/years')
def Years():
    year_data = session.query(extract('year', (tree_table.plant_date)),
        label('count', func.count(tree_table.tree_id))).filter(
            extract('year', (tree_table.plant_date)) > 0).group_by(
                extract('year', (tree_table.plant_date))).order_by(
                    extract('year', (tree_table.plant_date))).all()
    years = [{"names" : [c[0] for c in year_data],
          "counts" : [c[1] for c in year_data]}]
    return jsonify(years)  

@app.route('/caretakers')  
def Caretakers():
    caretaker_data = session.query(extract('caretaker', (tree_table.care_taker)),
        label('count', func.count(tree_table.tree_id))).filter(
            extract('caretaker', (tree_table.care_taker)) > 0).group_by(
                extract('caretaker', (tree_table.care_taker))).order_by(
                    extract('caretaker', (tree_table.care_taker))).all()
    years = [{"caretaker" : [c[0] for c in caretaker_data], "species_count" : [c[1] for c in caretaker_data]}]
    return jsonify(caretakers)


if __name__ == "__main__":
    app.run(debug=True)