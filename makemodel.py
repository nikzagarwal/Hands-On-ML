
from index import Modeldb
from index import Metricdb

import pandas as pd
import numpy as np  
import pickle
import requests
from sklearn import metrics
from random import randint
import os


def output(modeltype,model1,var_smoothing1,n_neighbors1,leaf_size1,max_depth1,min_samples_split1,n_estimators1,random_state1,max_leaf_nodes1,dftrainpath,ytrainpath,db):
    
    
    
    model=model1 
    X_train=pd.read_csv(dftrainpath)
    Y_train=pd.read_csv(ytrainpath)
    def naives(var_smoothing=1e-9):
        from sklearn.naive_bayes import GaussianNB


        clf=GaussianNB()
        clf.fit(X_train,Y_train)

        return clf



    def randomforest(n_estimators=500,max_leaf_nodes=None,min_samples_split=2):
        from sklearn.ensemble import RandomForestClassifier


        clf=RandomForestClassifier(n_estimators=n_estimators,max_leaf_nodes=max_leaf_nodes,min_samples_split=min_samples_split,n_jobs = -1)
        clf.fit(X_train,Y_train)

        return clf



    def knn(n_neighbors = 5 ,leaf_size = 30):
        from sklearn.neighbors import KNeighborsClassifier 



        clf=KNeighborsClassifier(n_neighbors=n_neighbors1,leaf_size=leaf_size1)
        clf.fit(X_train,Y_train)
    
        return clf



    #this is decision tress
    def decisiontrees(max_depth=None,min_samples_split=2):
        from sklearn.tree import DecisionTreeClassifier



        clf=DecisionTreeClassifier(max_depth=max_depth,min_samples_split=int(min_samples_split))
        clf.fit(X_train,Y_train)
        

        return clf


    #regression begins
    def randomforestreg(n_estimators=500,max_leaf_nodes=None):
        from sklearn.ensemble import RandomForestRegressor

        clf=RandomForestRegressor(n_estimators=n_estimators,max_leaf_nodes=max_leaf_nodes,n_jobs = -1)
        clf.fit(X_train,Y_train)

        return clf



    def knnreg(n_neighbors = 5 ,leaf_size = 30):
        from sklearn.neighbors import KNeighborsRegressor 

        clf=KNeighborsRegressor(n_neighbors=n_neighbors,leaf_size=leaf_size)
        clf.fit(X_train,Y_train)
    
        return clf




    def linearreg():
        from sklearn.linear_model import LinearRegression


        clf=LinearRegression()
        clf.fit(X_train,Y_train)
        

        return clf

    def decisiontreereg( max_depth=None,random_state=42,min_samples_split=2):
        from sklearn.tree import DecisionTreeRegressor

        clf=DecisionTreeRegressor(max_depth=max_depth,random_state=random_state,min_samples_split=int(min_samples_split))
        clf.fit(X_train,Y_train)
        

        return clf

    weightspath="static/weights/"+str(randint(0,9999999999))
    os.mkdir(weightspath)

    if model == 'naivebayes':
        
        clf=naives(var_smoothing=var_smoothing1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='decisiontrees':
        
        clf=decisiontrees(max_depth=max_depth1,min_samples_split=min_samples_split1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='knn':
        
        clf=knn(n_neighbors=n_neighbors1,leaf_size=leaf_size1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb')) 
        
    elif model=='randomforest':
        
        clf=randomforest(n_estimators=400 ,max_leaf_nodes=max_leaf_nodes1,min_samples_split=min_samples_split1) #as of now no parameters are passed
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model == 'linearreg':
        
        clf=linearreg()
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='decisiontreereg':
        
        clf=decisiontreereg(max_depth=max_depth1,random_state=random_state1,min_samples_split=min_samples_split1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='knnreg':
        
        clf=knnreg(n_neighbors=n_neighbors1,leaf_size=leaf_size1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb')) 
        
    elif model=='randomforestreg':
        
        clf=randomforestreg(n_estimators=n_neighbors1, max_leaf_nodes=max_leaf_nodes1) #as of now no parameters are passed
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
    model_accuracy=0
    model_f1_score=0
    model_precision=0
    model_recall=0
    y_pred=0
    model_rmse=0
    model_r2score=0
    if modeltype=="classification":
        y_pred=clf.predict(X_train)
        model_accuracy=metrics.accuracy_score(Y_train,y_pred.round())
        model_f1_score=metrics.f1_score(Y_train,y_pred.round())
        model_precision=metrics.precision_score(Y_train,y_pred.round())
        model_recall=metrics.recall_score(Y_train,y_pred.round())
    elif modeltype=="regression":
        y_pred=clf.predict(X_train)
        model_rmse=metrics.mean_squared_error(Y_train,y_pred)
        model_r2score=metrics.r2_score(Y_train,y_pred)


    x=Modeldb(modelType=modeltype,modelName=model, weights=weightspath+"/")
    db.session.add(x)
    db.session.commit()
    
    y=Metricdb(accuracy=model_accuracy,f1score=model_f1_score,precision=model_precision,recall=model_recall,rmse=model_rmse,r2=model_r2score,metricsid=x)
    db.session.add(y)
    db.session.commit()
    
    
    return x,y