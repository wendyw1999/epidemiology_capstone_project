# Pull data from repositories and store in temp.

import sys
import os
sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')
sys.path.insert(0, 'src/data/tmp')
from etl import *
from analysis import *
from model import *
import json

def main(targets):
    if 'data' in targets:
        from src.etl import get_data,get_county,get_state,get_country
        us_confirmed_df,us_death_df,global_recover_df,mobility = get_data()
        
        with open('config/data-params.json') as fh:
            data_cfg =json.load(fh)
        start = data_cfg["start"]
        days = data_cfg["days"]
        admin_level = data_cfg["admin_level"]
        admin_name = data_cfg["admin_name"]
        if admin_level == "state":
            s,i,r,p = get_state(start,days,admin_level,admin_name)
        elif admin_level == "county":
            s,i,r,p = get_county(start,days,admin_level,admin_name)
        elif admin_level == "country":
            s,i,r,p = get_country(start,days,admin_level,admin_name)
        

    if 'eda' in targets:
        with open('config/analysis-params.json') as fh:
            eda_cfg =json.load(fh)
            
            
    
    if 'model' in targets:
        #calculate m stats here
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)
        
            

    return

if __name__ == "__main__":
    targets=sys.argv[1:]
    main(targets)