import pandas as pd
import numpy as np

def read_txts():
    root = "data/temp/"
    filenames = ["us_removed", "us_population","us_susceptible","us_infected"]
    end = ".txt"
    us_removed = []
    us_population = []
    us_susceptible = []
    us_infected = []
    lis = [us_removed,us_population,us_susceptible,us_infected]
    for file,li in list(zip(filenames,lis)):
        
        li = read_txt(root + file+end)
        print(file+": number of entries: "+str(len(li)))
    #print("US_population:  "+us_population[0])
                              
def read_txt(filename):
    
    with open(filename, 'r') as f:
        items = f.read().split("\n")
    return items
        
    