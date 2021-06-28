#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

ct = pickle.load(open("ct.pkl", "rb"))
le = pickle.load(open("le.pkl", "rb"))
sc = pickle.load(open("sc.pkl", "rb"))

from catboost import CatBoostClassifier
cat = CatBoostClassifier(verbose=0)
cat.load_model("cat")

# In[77]:

#while 1:
filename = sys.argv[1]
real_data = pd.read_csv(filename,header=None, delimiter=" ")

dataset = real_data.copy()
real_data = real_data.drop(labels=[0,1,2,3,4,5,8],axis=1)

real_data


# In[78]:


real_data.columns = ["duration","protocol_type","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate"]


# In[79]:


x = real_data.iloc[:,:].values


# In[80]:


x = np.array(ct.transform(x))
x[:,15:] = sc.transform(x[:,15:])


# In[81]:


y =  le.inverse_transform(cat.predict(x))
indices = np.where(y=="attack")[0].tolist()


# In[82]:


j=0
for i in y:
	if i=="attack":
		j+=1
j


# In[83]:


attack_ips = dataset.iloc[indices,:].iloc[:,4].value_counts().keys().tolist()
attack_ip_counts = dataset.iloc[indices,:].iloc[:,4].value_counts().tolist()

total_ips = dataset.iloc[:,:].iloc[:,4].value_counts().keys().tolist()
total_ip_counts = dataset.iloc[:,:].iloc[:,4].value_counts().tolist()


# In[84]:


attack = { ip: count for ip, count in zip(attack_ips,attack_ip_counts)}
total = { ip: count for ip, count in zip(total_ips,total_ip_counts)}


# In[85]:


attack


# In[86]:


total


# In[87]:


block_ips = []
for ip in attack.keys():
	if attack[ip]/total[ip] > 0.2:
		block_ips.append(ip)

block_ips

f = open("ip.list", "w")
for ip in block_ips:
	f.write(ip + '\n')
f.close()

f = open("block.list", "a")
for ip in block_ips:
	f.write(ip + '\n')
f.close()




