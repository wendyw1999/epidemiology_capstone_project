import pandas as pd
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import json
def build_model(path):
    
    s_path = path+"s.txt"
    i_path = path+"i.txt"
    r_path = path+"r.txt"
    p_path = path+"p.txt"
    
    with open(s_path,"r") as f:
        s = f.read().split("\n")
        s = [int(x) for x in s if x!=""]
    with open(i_path,"r") as f:
        i = f.read().split("\n")
        i = [int(x) for x in i if x!=""]
    with open(r_path,"r") as f:
        r = f.read().split("\n")
        r = [int(x) for x in r if x!=""]
        
    with open(p_path,"r") as f:
        p = f.read().split("\n")[0]
        p = int(p)
    with open('config/model_params.json') as fh:
        model_cfg = json.load(fh)

    iterations = model_cfg["iterations"]
    iterations = 10000
    learning_rate1 = 1e-3/p * 60
    learning_rate2 = 1e-3/p * 60
    betas,d = calculate(s,i,r,p,learning_rate1,learning_rate2,iterations)
    return betas,d
    
    
def tune_learning_rate(s,i,r,p,iterations):
    learning_rate1 = 1e-3/p * 60
    learning_rate2 = 1e-3/p * 60
    betas = []
    ds = []
    while isinstance(betas,list) and isinstance(ds,list):
        learning_rate1 = learning_rate1/10
        learning_rate2 = learning_rate2/10
        betas,ds = calculate(s,i,r,p,learning_rate1,learning_rate2,iterations)
    while isinstance(ds,list):
        learning_rate2 = learning_rate2/10
        betas,ds = calculate(s,i,r,p,learning_rate1,learning_rate2,iterations)
    while isinstance(ds,list):
        learning_rate1 = learning_rate1/10
        betas,ds = calculate(s,i,r,p,learning_rate1,learning_rate2,iterations)   
    return betas,ds
def calculate_gradient(s,i,r,population,beta,epsilon):
    result1 = 0 #continue adding to solve for beta
    result2 = 0 #continue adding to solve for 1/D aka epsilon
    for n in range(len(s)-1):
        result1 += 2*(s[n+1]-s[n]+beta*s[n]*(i[n]/population))*(s[n]*i[n]/population)
        result1 += 2*(i[n+1]-i[n]-beta*s[n]*(i[n]/population) + i[n]*epsilon)*(-s[n]*i[n]/population)
        
        result2 += 2*(i[n+1]-i[n]+i[n]*epsilon-beta*i[n]*s[n]/population)*(i[n])
        result2 += 2*(r[n+1]-r[n]-i[n]*epsilon)*(-i[n])
        
    return result1,result2
def calculate(s,i,r,population,learning_rate1,learning_rate2,iterations):
    beta = 0.2
    epsilon = 1/14
    
    loss = 0
    length = len(s)
    betas = []
    ds = []
    
    for itera in range(iterations): # do it for 10 iterations.
        
        loss1,loss2 = calculate_gradient(s,i,r,population,beta,epsilon)
        beta_new = beta - learning_rate1* loss1/length #0.001 is the learning rate
        epsilon_new = epsilon - learning_rate2 * loss2/length
        if (beta_new == beta) & (epsilon_new == epsilon):
            
            return beta_new,1/epsilon_new
           
        beta = beta_new
        epsilon = epsilon_new
        
        betas.append(beta)
        ds.append(1/epsilon)

    return betas,ds

