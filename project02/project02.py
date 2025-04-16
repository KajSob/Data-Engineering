#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re


# In[2]:


check = 0
df = pd.read_csv('proj2_data.csv', sep = ";")
if df.columns.size == 1:
    df = pd.read_csv('proj2_data.csv', sep = "|")
if df.columns.size == 1:
    df = pd.read_csv('proj2_data.csv', sep = ",")

for i in df.dtypes:
    if i == 'float64':
        check = 1
if check == 0:
    df = pd.read_csv('proj2_data.csv', sep = ";",decimal=',')
    if df.columns.size == 1:
        df = pd.read_csv('proj2_data.csv', sep = "|",decimal=',')


# In[3]:


df.dtypes


# In[4]:


df.head()


# In[5]:


df.to_pickle("proj2_ex01.pkl")


# In[6]:


df2 = df.copy()


# In[7]:


df2.head()


# In[8]:


my_file = open("proj2_scale.txt", "r") 
data = my_file.read() 
helplist = data.split("\n") 
my_file.close() 


# In[9]:


helplist


# In[10]:


for col in df2:
    if all(val in helplist for val in df2[col]):
        for val in df2[col]:
            df2[col] = df2[col].replace([val], str(helplist.index(val) + 1))
        df2[col] = df2[col].astype(int)


# In[11]:


df2.head()


# In[12]:


df2.dtypes


# In[13]:


df2.to_pickle("proj2_ex02.pkl")


# In[14]:


df3 = df.copy()


# In[15]:


df3.head()


# In[16]:


for col in df3:
    if all(val in helplist for val in df3[col]):
        df3[col] = df3[col].astype("category")
        df3[col] = df3[col].cat.set_categories(helplist)


# In[17]:


df3.dtypes


# In[18]:


df3.to_pickle("proj2_ex03.pkl")


# In[19]:


def lounge_control(dude):
    vipcard = r'[-]?\d*[\.,]?\d+'
    checkout = re.search(vipcard, dude)
    if checkout:
        return float(checkout.group().replace(',','.'))
    else:
        return None


# In[20]:


df_copy = df.copy()


# In[21]:


df4 = pd.DataFrame()


# In[22]:


for col in df.select_dtypes(include=['object']):
    new_batch = df_copy[col].apply(lounge_control)
    if any(val != None for val in new_batch):
        df4[col] = new_batch


# In[23]:


df4


# In[24]:


df4.to_pickle("proj2_ex04.pkl")


# In[25]:


counter = 1
for col in df.select_dtypes(include=['object']):
    if len(df[col].unique())<=10:
        if all(re.search(r'^[a-z]+$',val) for val in df[col]):
            if any(val not in helplist for val in df[col]):
                enigma = pd.get_dummies(df[col], prefix="", prefix_sep="")
                print(enigma)
                enigma.to_pickle(f'proj2_ex05_{counter}.pkl')
                counter+=1


# In[ ]:




