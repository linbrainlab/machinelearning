#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 18:19:24 2018

@author: XIN
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

@author: XIN
"""

#Features without image features:


import matplotlib.pyplot as plt

from sklearn import svm
from scipy import interp
import numpy as np
import pandas as pd
from itertools import cycle

from sklearn.ensemble import (RandomForestClassifier,
                              GradientBoostingClassifier)
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import resample
from sklearn.utils import shuffle
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score
#from imblearn.combine import SMOTEENN
#from imblearn.over_sampling import SMOTE 




#original data
#data=pd.read_csv('/Users/xinxing/Documents/XIN/Work/DrLin/ADNI/NewData/combined_norm_features_final.csv',encoding='mac_greek').fillna(0)

#corviate balancing data
data=pd.read_csv('/Users/xinxing/Documents/XIN/Work/DrLin/ADNI/NewData/cobal.csv',encoding='mac_greek').fillna(0)

#1. All feature
df=data[['DX','FDG-Angular','FDG-Temporal','FDG-CingulumPost','Entorhinal','Hippocampus','Aß-Cingulate','Aß-Frontal','Aß-Parietal','Aß-Temporal','Aß-Hippocampus','Aß-Precuneus','Ventricles','WBV','WMV','GMV','pTau']]

#Top 8 features
#CN vs LMCI
#df=data[['DX','FDG-Angular','Aß-Cingulate','Aß-Frontal','Aß-Temporal','Aß-Precuneus','pTau','Entorhinal','Hippocampus']]

#LMCI vs AD
#df=data[['DX','FDG-Angular','FDG-Temporal','FDG-CingulumPost','pTau','Entorhinal','Hippocampus','Aß-Temporal','Aß-Precuneus']]

#CN vs. AD
#df=data[['DX','FDG-Angular','FDG-Temporal','FDG-CingulumPost','pTau','Entorhinal','Hippocampus','Aß-Temporal','Aß-Precuneus']]

df_CN=df[df.DX==0] 
df_EMCI=df[df.DX==1] 
df_LMCI=df[df.DX==2] 
df_AD=df[df.DX==3]
#df_MCI=pd.concat([df_LMCI, df_EMCI])
#df['DX'].value_counts()

#Try the original:
df_sampled=pd.concat([df_CN, df_LMCI])
df_sampled=shuffle(df_sampled)
y=df_sampled.DX
X=df_sampled.drop('DX',axis=1)
X_1=df_sampled.drop('DX',axis=1)
#b=np.mean(importance, axis=0)
#feature_importances = pd.DataFrame(b,index = X_1.columns, columns=['importance']).sort_values('importance',ascending=False)

y = label_binarize(y, classes=[0, 2])

numFeature=X.shape[1]
#X=X.as_matrix()
y=y.ravel()
#normalized standardize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X=scaler.transform(X)



#clf=RandomForestClassifier(n_estimators=100,criterion='entropy')#,class_weight='balanced')
#clf=svm.SVC(kernel='rbf',C=1000, gamma=0.01,coef0=0.01,probability=True)
#cv = StratifiedKFold(n_splits=3)
tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 250)
result= []
importance=np.zeros((10,numFeature))
res=[]
f1=[]

i = 0
j=0 
for i in range(100):
    #clf=RandomForestClassifier(n_estimators=3600, min_samples_split=5, min_samples_leaf=8, max_features='auto',max_depth=50, bootstrap=False)
    clf = GradientBoostingClassifier(n_estimators=3600, min_samples_split=5, min_samples_leaf=8, max_features='auto',max_depth=50)
    cv = StratifiedKFold(n_splits=10)
    for train, test in cv.split(X, y):
    
        #sm= SMOTEENN(random_state=44)
        #X_res,y_res=sm.fit_sample(X[train],y[train])
        #probas_ = clf.fit(X_res, y_res).predict_proba(X[test])#The smote upsampling
        probas_ = clf.fit(X[train], y[train]).predict_proba(X[test]) #original
        accuracy=clf.predict(X[test])
        res.append(clf.score(X[test],y[test]))
        #print(('accuracy: ')+str(clf.score(X[test],y[test])))
        y_pred=clf.predict(X[test])
        f1.append(f1_score(y[test], y_pred, average='weighted'))
        #print(('F1 socre: ')+str(f1_score(y[test], y_pred, average='weighted')))
        importance[j,:]=clf.feature_importances_
        
        j += 1
    i += 1
b=np.mean(importance, axis=0)
feature_importances = pd.DataFrame(b,index = X_1.columns, columns=['importance']).sort_values('importance',ascending=False)    
print("The acc is: "+str(np.mean(res)))
print("The f1 is: " +str(np.mean(f1)))
print("The feature ranking is:")
print(feature_importances)


