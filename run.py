# Pull data from repositories and store in temp.
import sys
import os
from all_function import *
import json

def main(targets):
    if 'data' in targets:
        
        with open('config/data-params.json') as fh:
            data_cfg =json.load(fh)
        

    if 'eda' in targets:
        with open('config/analysis-params.json') as fh:
            eda_cfg =json.load(fh)
            
            
    
    if 'model' in targets:
        #calculate m stats here
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)
            

    return

if __name__ == "__main__":
    targets=sys.argv[1: ]
    main(targets)