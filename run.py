# Pull data from repositories and store in temp.

import sys
import os
sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')
sys.path.insert(0, 'src/data/tmp')
from etl import *
import json
from src.data.etl import *
from src.model.train_model import *


def main(targets):
    if 'data' in targets:
        path = "test/testdata/"
        collect_data(path)
        print("Done downloading data to :"+path)
    if "test" in targets:
        collect_data("test/testdata/")
        print("done downloading data")
        beta,d = build_model("test/testdata/")
        print("beta is:  "+str(beta))
        print("D is :   "+str(d))
        
    if 'model' in targets:
        #calculate m stats here
        beta,d = build_model("test/testdata/")
        print("beta is:  "+str(beta))
        print("D is :   "+str(d))
              
        
            
    if 'eda' in targets:
        with open('config/analysis-params.json') as fh:
            eda_cfg =json.load(fh)

    return

if __name__ == "__main__":
    targets=sys.argv[1:]
    main(targets)
