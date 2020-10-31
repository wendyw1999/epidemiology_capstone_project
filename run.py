# Pull data from repositories and store in temp.
import sys
from src.data.etl import download_data,clean_data
from src.analysis.analysis import read_txts
import json
if __name__ == "__main__":
    command = sys.argv[1]
    
    if command == "data":
      
        with open("config/data-params.json", "r") as read_file:
            data_param= json.load(read_file)  
        print("Retrieving Data...")
        download_data(data_param)
        
    