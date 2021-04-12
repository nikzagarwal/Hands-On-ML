
def cleanpy2(cols,changetype,encodecol,scaling,scalingcol,targetcol,dftest,cleandatapath,rawdatapath):
    import pandas as pd
    import numpy as np
    from sklearn import preprocessing
    import os
    cols=cols
    changetype=changetype
    encodecol=encodecol
    scaling=scaling
    scalingcol=scalingcol
    targetcol=[targetcol]
    dftest=""

    df=pd.read_csv(rawdatapath)
    #feature scaling
    if(scalingcol[0]!="none"):
        if scaling=='standarization':
            for feature in scalingcol:
                df[feature] = (df[feature] - df[feature].mean()) / (df[feature].std())
        else:
            x = df[scalingcol].values #returns a numpy array
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            df[scalingcol]= x_scaled

    #encoding
   
    le = preprocessing.LabelEncoder()
    if(encodecol[0]!="none"):
        if changetype=="labelencode":
            featurex=df[encodecol]
            featurex=featurex.apply(le.fit_transform)
            features=featurex.columns
            for feature in features:
                df.drop([feature],axis=1,inplace=True)
                df=pd.concat([df,featurex[feature]],axis=1)
        else:
            dummy=pd.get_dummies(df[encodecol])
            df=pd.concat([df,dummy],axis=1)
            df.drop(encodecol,axis=1,inplace=True)
    if df[df[targetcol].columns[0]].dtype==object:
        featurex=df[targetcol]
        featurex=featurex.apply(le.fit_transform)
        features=featurex.columns
        for feature in features:
             df.drop([feature],axis=1,inplace=True)
             df=pd.concat([df,featurex[feature]],axis=1) 

    # drop columns
    if(cols[0]!="none"):
        df=df.drop(cols, axis = 1)


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
    ytrain=pd.DataFrame(dftrain[targetcol])
    ytest=pd.DataFrame(dftest[targetcol])
    dftrain.drop(targetcol,axis=1,inplace=True)
    dftest.drop(targetcol,axis=1,inplace=True)
    
    
    dftrain.to_csv(cleandatapath+"dftrain.csv",index=None)
    dftest.to_csv(cleandatapath+"dftest.csv",index=None)
    ytrain.to_csv(cleandatapath+"ytrain.csv",index=None)
    ytest.to_csv(cleandatapath+"ytest.csv",index=None)


    
    


