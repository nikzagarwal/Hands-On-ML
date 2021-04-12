
def cleanpy(cols,changetype,encodecol,scaling,scalingcol,targetcol,dftest,cleandatapath,rawdatapath):
    import pandas as pd
    import numpy as np
    from sklearn import preprocessing
    import os

    df=pd.read_csv(rawdatapath)
    origcol=df.columns

    if(cols!=""):
        cols=cols.split(",")
        cols = list(map(int, cols))
    if(encodecol!=""):
        encodecol=encodecol.split(",")
        encodecol = list(map(int, encodecol))
    if(scalingcol!=""):
        scalingcol=scalingcol.split(",")
        scalingcol = list(map(int, scalingcol))
    targetcol = list(map(int, targetcol))

    #feature scaling
    if(scalingcol!=""):
        if scaling=='standarization':
            for feature in scalingcol:
                df.iloc[:,feature] = (df.iloc[:,feature] - df.iloc[:,feature].mean()) / (df.iloc[:,feature].std())
        else:
            x = df.iloc[:,scalingcol].values #returns a numpy array
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            df.iloc[:,scalingcol]= x_scaled

    #encoding
    le = preprocessing.LabelEncoder()
    if(encodecol!=""):
        if changetype=="labelencode":
            featurex=df.iloc[:,encodecol]
            featurex=featurex.apply(le.fit_transform)
            features=featurex.columns
            for feature in features:
                df.drop([feature],axis=1,inplace=True)
                df=pd.concat([df,featurex[feature]],axis=1)
        else:
            dummy=pd.get_dummies(df.iloc[:,encodecol])
            df=pd.concat([df,dummy],axis=1)
            df.drop(origcol[encodecol],axis=1,inplace=True)
    if df[df.iloc[:,targetcol].columns[0]].dtype==object:
        featurex=df.iloc[:,targetcol]
        featurex=featurex.apply(le.fit_transform)
        features=featurex.columns
        for feature in features:
             df.drop([feature],axis=1,inplace=True)
             df=pd.concat([df,featurex[feature]],axis=1) 

    # drop columns
    if(cols!=""):
        df=df.drop(origcol[cols], axis = 1)


    #  mandatory cleaning

    # removing rows having null values
    df.dropna(inplace=True) 
    # try to convert all non-numeric values to numeric if possible
    df=df.infer_objects()
    # removing columns having object type values as it will create problem in model creation
    removecol=df.select_dtypes(include=['object']).columns
    df.drop(labels=removecol,axis=1,inplace=True)

    #test data creation
    if dftest=="":
        msk=np.random.rand(len(df))<0.75
        dftrain=df[msk]
        dftest=df[~msk]  
    else:
        dftrain=df
    #target variable seperation
    ytrain=pd.DataFrame(dftrain[origcol[targetcol][0]])
    ytest=pd.DataFrame(dftest[origcol[targetcol][0]])
    dftrain.drop([origcol[targetcol][0]],axis=1,inplace=True)
    dftest.drop([origcol[targetcol][0]],axis=1,inplace=True)
    
    
    dftrain.to_csv(cleandatapath+"dftrain.csv",index=None)
    dftest.to_csv(cleandatapath+"dftest.csv",index=None)
    ytrain.to_csv(cleandatapath+"ytrain.csv",index=None)
    ytest.to_csv(cleandatapath+"ytest.csv",index=None)

    
    


