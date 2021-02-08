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
from src.model.predict_model import *
from src.analysis.analysis import *

def main(targets):
    if 'data' in targets:
        if not os.path.exists('data'):
            os.makedirs('data')
        
        path = "data"
        collect_data(path)
        print("Done downloading data to :"+path)
    if "test" in targets:
        if not os.path.exists('test'):
            os.makedirs('test')
        if not os.path.exists('test/testdata'):
            os.makedirs("test/testdata")
        #collect data
        collect_data("test/testdata/")
        print("done downloading data")
        
        #fitting the model
        beta,d = build_model("test/testdata/")
        print("beta is:  "+str(beta))
        print("D is :   "+str(d))
        
        #Analysis and ploting
        with open('config/analysis_params.json') as fh:
            eda_cfg =json.load(fh)
        data_path = eda_cfg["test_data_path"]
        output_path = eda_cfg["test_img_path"]
        draw_ODE(data_path,output_path,beta,d) #Generate a plot in the test  folder from data in the test/testdata folder
        
        
        print("Mean Absolute Percentage Error" + str(print_prediction_error()))
        
    
    if 'model' in targets:
        #calculate m stats here
        beta,d = build_model("test/testdata/")
        print("beta is:  "+str(beta))
        print("D is :   "+str(d))
              
        
            
    #if 'eda' in targets:
        

    return

if __name__ == "__main__":
    targets=sys.argv[1:]
    main(targets)
