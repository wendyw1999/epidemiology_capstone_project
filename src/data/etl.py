import pandas as pd
import numpy as np
import os
def pull_data():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    us_confirmed_df = pd.read_csv(url, error_bad_lines=False)
    us_confirmed_df.to_csv("data/temp/us_confirmed.csv")
    print("Downloaded to data/temp/us_confirmed.csv")
    
    
    
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    us_death_df = pd.read_csv(url, error_bad_lines=False)
    us_death_df.to_csv("data/temp/us_death.csv")
    print("Downloaded to data/temp/us_death.csv")
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    global_recover_df = pd.read_csv(url, error_bad_lines=False)
    global_recover_df.to_csv("data/temp/global_recover.csv")
    print("Downloaded to data/temp/global_recover.csv")

    url = "https://raw.githubusercontent.com/descarteslabs/DL-COVID-19/master/DL-us-m50.csv"
    mobility = pd.read_csv(url, error_bad_lines=False)
    mobility.to_csv("data/temp/mobility.csv")
    print("Downloaded to data/temp/mobility.csv")

def download_data(data_param):
    
    
    
    
    for i in data_param.keys():
        url = data_param[i]
        
        df = pd.read_csv(url, error_bad_lines=False)
        #do something here
        print(df.head())
        print("DataFrame :"+i)

def clean_data(us_confirmed_df,us_death_df,global_recover_df):
    # Data Preparation
    us_confirmed = us_confirmed_df.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis=1).sum(axis=0).values
    us_death = us_death_df.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key',"Population"],axis=1).sum(axis=0).values
    us_recovered = global_recover_df.loc[global_recover_df["Country/Region"] == "US"].drop(
        ["Province/State","Country/Region","Lat","Long"],axis= 1).values[0]
    #us_removed = us_recovered+us_death
    us_removed = us_recovered+us_death
    us_population = us_death_df.Population.sum()
    us_susceptible = us_population - us_confirmed
    us_infected = us_confirmed

    
    array = [us_removed, [us_population],us_susceptible,us_infected]
    root = "data/temp/"
    filenames = ["us_removed.txt", "us_population.txt","us_susceptible.txt","us_infected.txt"]
        
    for filename,my_list in list(zip(filenames,array)):
        write_list_to_txt(root+filename,my_list)
def write_list_to_txt(filename,my_list):

    with open(filename, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
    print("txt file at:  "+filename)

