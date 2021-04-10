
from app import Modeldb
from app import Metricdb

import pandas as pd
import numpy as np  
import pickle
import requests
from sklearn import metrics
from random import randint
import os


def output(modeltype,model1,dftrainpath,ytrainpath,dftestpath,ytestpath,db,num,alpha1=1,n_neighbors1=5,leaf_size1=30,max_depth1=50,min_samples_split1=2,n_estimators1=500,random_state1=42,max_leaf_nodes1=50):
    
    
    
    model=model1 
    X_train=pd.read_csv(dftrainpath)
    Y_train=pd.read_csv(ytrainpath)
    X_test=pd.read_csv(dftestpath)
    Y_test=pd.read_csv(ytestpath)

    def naives(alpha=1.0):
        from sklearn.naive_bayes import MultinomialNB

        clf=MultinomialNB(alpha=alpha1)
        clf.fit(X_train,Y_train.values.ravel())

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

    if model == 'Naive Bayes':
        
        clf=naives(alpha=alpha1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='Decision Trees':
        
        clf=decisiontrees(max_depth=max_depth1,min_samples_split=min_samples_split1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='Knn':
        
        clf=knn(n_neighbors=n_neighbors1,leaf_size=leaf_size1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb')) 
        
    elif model=='Random Forest':
        
        clf=randomforest(n_estimators=400 ,max_leaf_nodes=max_leaf_nodes1,min_samples_split=min_samples_split1) #as of now no parameters are passed
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model == 'Linear Regression':
        
        clf=linearreg()
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='Decision Tree Regression':
        
        clf=decisiontreereg(max_depth=max_depth1,random_state=random_state1,min_samples_split=min_samples_split1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb'))
        
    elif model=='Knn Regression':
        
        clf=knnreg(n_neighbors=n_neighbors1,leaf_size=leaf_size1)
        pickle.dump(clf,open(weightspath+'/model.pkl','wb'))
        #modelf=pickle.load(open('model.pkl','rb')) 
        
    elif model=='Random Forest Regression':
        
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
        y_pred=clf.predict(X_test)
        model_accuracy=metrics.accuracy_score(Y_test,y_pred)
        model_f1_score=metrics.f1_score(Y_test,y_pred,average='micro')
        model_precision=metrics.precision_score(Y_test,y_pred,average='micro')
        model_recall=metrics.recall_score(Y_test,y_pred,average='micro')
    elif modeltype=="regression":
        y_pred=clf.predict(X_test)
        model_rmse=metrics.mean_squared_error(Y_test,y_pred)
        model_r2score=metrics.r2_score(Y_test,y_pred)


    x=Modeldb(modelType=modeltype,modelName=model, weights=weightspath+"/",common=num)
    db.session.add(x)
    db.session.commit()
    
    y=Metricdb(accuracy=model_accuracy,f1score=model_f1_score,precision=model_precision,recall=model_recall,rmse=model_rmse,r2=model_r2score,metricsid=x,common=num)
    db.session.add(y)
    db.session.commit()
    
    
    return x,y