import pandas as pd
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import json
from numpy import linalg as LA
def build_model(path):
    '''
    the overall method that will collect data from local files, and read params from json file, and do the model training
    path: takes in the path where the s,i,r,p text files are located (a folder name)
    returns: model parameters beta and d
    beta is the infection rate
    d is the infectious duration
    '''
    
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

    
    learning_rate = tune_learning_rate(s,i,r,p)
    betas,d = calculate(s,i,r,p,learning_rate,iterations)
    return betas,d
    
def calculate_hessian(s,i,r,population):
    '''
    create hessian matrix (second derivatives of beta and d)
    '''
    result_beta_second = 0
    result_epsilon_second = 0
    result_both_second = 0
    for n in range(len(s)-1):
        result_beta_second += 4*(s[n] * i[n]/population) **2 
        result_epsilon_second += 4*i[n]
        result_both_second += -2*s[n]*i[n]**2/population
    return result_beta_second/len(s),result_epsilon_second/len(s),result_both_second/len(s)
            
def tune_learning_rate(s,i,r,p):
    '''
    calculate 0.1/eigenvalue of hessian matrix, our learning rate
    '''
    
    top_left,bottom_right,the_other_two = calculate_hessian(s,i,r,p)
    w, v = LA.eigh(np.array([[top_left, the_other_two], [the_other_two, bottom_right]]))
    lip_constant = w[w>0][0]
    return 0.1/lip_constant

def calculate_gradient(s,i,r,population,beta,epsilon):
    '''
    get gradients at each iteration of gradient descent
    '''
    result1 = 0 #continue adding to solve for beta
    result2 = 0 #continue adding to solve for 1/D aka epsilon
    for n in range(len(s)-1):
        result1 += 2*(s[n+1]-s[n]+beta*s[n]*(i[n]/population))*(s[n]*i[n]/population)
        result1 += 2*(i[n+1]-i[n]-beta*s[n]*(i[n]/population) + i[n]*epsilon)*(-s[n]*i[n]/population)
        
        result2 += 2*(i[n+1]-i[n]+i[n]*epsilon-beta*i[n]*s[n]/population)*(i[n])
        result2 += 2*(r[n+1]-r[n]-i[n]*epsilon)*(-i[n])
        
    return result1,result2
def calculate(s,i,r,population,learning_rate,iterations):
    '''
    gradient descent method
    returns: beta and d
    we initialized beta to be 0.2 and D to 14 from existing knowledge so we can get to convergence faster
    '''
    beta = 0.2
    epsilon = 1/14
    
    loss = 0
    length = len(s)
    betas = []
    ds = []
    
    for itera in range(iterations): # do it for 10 iterations.
        
        loss1,loss2 = calculate_gradient(s,i,r,population,beta,epsilon)
        beta_new = beta - learning_rate* loss1/length #0.001 is the learning rate
        epsilon_new = epsilon - learning_rate * loss2/length
        if (beta_new == beta) & (epsilon_new == epsilon):
            return beta_new,1/epsilon_new
           
        beta = beta_new
        epsilon = epsilon_new
        
        betas.append(beta)
        ds.append(1/epsilon)
        
    return betas,ds

