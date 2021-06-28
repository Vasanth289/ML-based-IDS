#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

train_path="KDDTrain++.TXT"
test_path="KDDTest+.txt"

col_names = ["duration","protocol_type","service","flag","src_bytes",
"dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
"logged_in","num_compromised","root_shell","su_attempted","num_root",
"num_file_creations","num_shells","num_access_files","num_outbound_cmds",
"is_host_login","is_guest_login","count","srv_count","serror_rate",
"srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
"diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
"dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
"dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]


train_data = pd.read_csv(train_path,header=None, names=col_names)
test_data = pd.read_csv(test_path,header=None, names=col_names) 
train_data = train_data.drop(["difficulty", "service"], axis=1)
test_data = test_data.drop(["difficulty", "service"], axis=1)


train_data = train_data.replace(to_replace = ['neptune', 'warezclient', 'ipsweep', 'portsweep', 'teardrop', 'nmap', 'satan', 'smurf', 'pod', 'back',
   'guess_passwd', 'ftp_write', 'multihop', 'rootkit', 'buffer_overflow', 'imap', 'warezmaster', 'phf', 'land',
   'loadmodule', 'spy', 'perl'], value = "attack")

test_data = test_data.replace(to_replace = ['neptune', 'saint', 'mscan', 'guess_passwd', 'smurf',
   'apache2', 'satan', 'buffer_overflow', 'back', 'warezmaster',
   'snmpgetattack', 'processtable', 'pod', 'httptunnel', 'nmap', 'ps',
   'snmpguess', 'ipsweep', 'mailbomb', 'portsweep', 'multihop',
   'named', 'sendmail', 'loadmodule', 'xterm', 'worm', 'teardrop',
   'rootkit', 'xlock', 'perl', 'land', 'xsnoop', 'sqlattack',
   'ftp_write', 'imap', 'udpstorm', 'phf'], value = "attack")

X_train = train_data.iloc[:,:-1].values
y_train = train_data.iloc[:, -1].values

X_test = test_data.iloc[:,:-1].values
y_test = test_data.iloc[:, -1].values

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1,2])], remainder='passthrough')
ct.fit(X_train)
pickle.dump(ct, open("ct.pkl", "wb"))
X_train = np.array(ct.transform(X_train))
X_test = np.array(ct.transform(X_test))

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(y_train)
pickle.dump(le, open("le.pkl", "wb"))
y_train = le.transform(y_train)
y_test = le.transform(y_test)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train[:,15:])
pickle.dump(sc, open("sc.pkl", "wb"))
X_train[:,15:] = sc.transform(X_train[:,15:])
X_test[:,15:] = sc.transform(X_test[:,15:])

X_train.shape, y_train.shape, X_test.shape, y_test.shape


# In[2]:


# Catboost 
from sklearn.metrics import confusion_matrix, classification_report
print("CatBoost Model training....")
from catboost import CatBoostClassifier
cat = CatBoostClassifier(verbose=0)

cat.fit(X_train, y_train)
cat.save_model("cat")
y_pred = cat.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print('Confusion matrix:\n',cm)
print()
print('Classification report:\n',classification_report(y_test,y_pred))





