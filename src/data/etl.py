import pandas as pd
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import os
import json

def collect_data(path):
    us_confirmed_df,us_death_df,global_recover_df,mobility = retrieve_data()
    with open('config/data-params.json') as fh:
        data_cfg =json.load(fh)
    start = data_cfg["start"]
    days = data_cfg["days"]
    admin_level = data_cfg["admin_level"]
    admin_name = data_cfg["admin_name"]
    df_list = [us_confirmed_df,us_death_df,global_recover_df]
    if admin_level == "state":
        s,i,r,p = get_state(start,days,df_list,admin_name)
    elif admin_level == "county":
        s,i,r,p = get_county(start,days,df_list,admin_name)
    elif admin_level == "country":
        s,i,r,p = get_country(start,days,df_list,admin_name)
    s_path = path+"s.txt"
    i_path = path+"i.txt"
    r_path = path+"r.txt"
    p_path = path+"p.txt"
    write_list_to_txt(s_path,s)
    write_list_to_txt(i_path,i)
    write_list_to_txt(r_path,r)
    write_list_to_txt(p_path,[p])
    return path
    
def retrieve_data():
    '''
    retrieves information from the JHU and mobility data repository
    '''
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    us_confirmed_df = pd.read_csv(url, error_bad_lines=False)

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    us_death_df = pd.read_csv(url, error_bad_lines=False)



    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    global_recover_df = pd.read_csv(url, error_bad_lines=False)



    url = "https://raw.githubusercontent.com/descarteslabs/DL-COVID-19/master/DL-us-m50.csv"
    mobility = pd.read_csv(url, error_bad_lines=False)

    us_confirmed_df = us_confirmed_df.loc[us_confirmed_df.Admin2 != "Unassigned"]
    us_death_df = us_death_df.loc[us_death_df.Admin2 != "Unassigned"]
    return us_confirmed_df,us_death_df,global_recover_df,mobility





def get_county(start,days,df_list,county_code = 1001):
    us_confirmed_df = df_list[0]
    us_death_df = df_list[1]
    global_recover_df = df_list[2]
    county_confirmed = us_confirmed_df.loc[us_confirmed_df.FIPS == county_code].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis=1).sum(axis=0).values
    county_death = us_death_df.loc[us_death_df.FIPS == county_code].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key',"Population"],axis=1).sum(axis=0).values
    county_population = us_death_df.loc[us_death_df.FIPS ==county_code].Population.sum()
    county_infected = county_confirmed
    county_removed = county_death
    county_susceptible = county_population - county_infected
    return county_susceptible[start:days+start],county_infected[start:start+days],county_removed[start:start+days],county_population

def get_state(start,days,df_list,state_name = "Washington"):
    us_confirmed_df = df_list[0]
    us_death_df = df_list[1]
    global_recover_df = df_list[2]    
    county_confirmed = us_confirmed_df.loc[us_confirmed_df.Province_State == state_name].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis=1).sum(axis=0).values
    county_death = us_death_df.loc[us_death_df.Province_State == state_name].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key',"Population"],axis=1).sum(axis=0).values
    county_population = us_death_df.loc[us_death_df.Province_State ==state_name].Population.sum()
    county_infected = county_confirmed
    county_removed = county_death
    county_susceptible = county_population - county_infected
    return county_susceptible[start:start + days],county_infected[start:start + days],county_removed[start:days+start],county_population
def get_country(start,days,df_list,country_name = "US"):
    us_confirmed_df = df_list[0]
    us_death_df = df_list[1]
    global_recover_df = df_list[2]   
    county_confirmed = us_confirmed_df.loc[us_confirmed_df.Country_Region == country_name].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis=1).sum(axis=0).values
    county_death = us_death_df.loc[us_death_df.Country_Region == country_name].drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
           'Country_Region', 'Lat', 'Long_', 'Combined_Key',"Population"],axis=1).sum(axis=0).values
    county_population = us_death_df.loc[us_death_df.Country_Region ==country_name].Population.sum()
    country_recovered = global_recover_df.loc[global_recover_df["Country/Region"] == country_name].drop(
    ["Province/State","Country/Region","Lat","Long"],axis= 1).values[0]
    county_infected = county_confirmed
    county_removed = county_death + country_recovered
    county_susceptible = county_population - county_infected
    return county_susceptible[start:start+days],county_infected[start:start+days],county_removed[start:start+days],county_population

def write_list_to_txt(filename,my_list):

    with open(filename, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
    print("txt file at:  "+filename)

