def getoptionpy(rawdatapath):
    import pandas as pd
    import numpy as np
    from sklearn import preprocessing

    df=pd.read_csv(rawdatapath)
    origcol=df.columns.tolist()
    origcol.insert(0,"none")
    return origcol
