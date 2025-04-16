#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json


# In[2]:


f = open('proj5_params.json')
params = json.load(f)
f.close()
params


# In[3]:


df1 = pd.read_csv('proj5_timeseries.csv', sep = ",")


# In[4]:


df1.columns = df1.columns.str.lower().str.replace(r'[^a-z]', '_', regex=True)


# In[5]:


df1['date'] = pd.to_datetime(df1['date'], format='mixed')
df1


# In[6]:


df1 = df1.set_index(df1.columns[0])


# In[7]:


df1


# In[8]:


df1 = df1.asfreq(params['original_frequency'])


# In[9]:


df1.to_pickle("proj5_ex01.pkl")


# In[10]:


df2 = df1.asfreq(params['target_frequency'])


# In[11]:


df2


# In[12]:


df2.to_pickle("proj5_ex02.pkl")


# In[13]:


def sumnan(ar):
    if ar.isna().any():
        return np.nan
    else:
        return ar.sum()
        


# In[14]:


df3 = df1.resample(f'{params["downsample_periods"]}{params["downsample_units"]}').apply(sumnan)


# In[15]:


df3


# In[16]:


df3.to_pickle("proj5_ex03.pkl")


# In[17]:


params


# In[18]:


df4 = df1.resample(f'{params["upsample_periods"]}{params["upsample_units"]}').interpolate(params["interpolation"], order=params["interpolation_order"])


# In[19]:


df4


# In[20]:


base = pd.Timedelta(1, unit=params["original_frequency"])
new = pd.Timedelta(f'{params["upsample_periods"]}{params["upsample_units"]}')
scale = new / base


# In[21]:


scale


# In[22]:


base


# In[23]:


new


# In[24]:


df4 = df4 * scale


# In[25]:


df4


# In[26]:


df4.to_pickle("proj5_ex04.pkl")


# In[27]:


df5 = pd.read_pickle('proj5_sensors.pkl')


# In[28]:


df5 = df5.pivot(columns='device_id', values='value')
df5


# In[29]:


oonit = f'{params["sensors_periods"]}{params["sensors_units"]}'



# In[30]:


new_index = pd.date_range(df5.index.round(oonit).min(), df5.index.round(oonit).max(), freq=oonit)


# In[31]:


new_index


# In[32]:


df52 = df5.reindex(new_index.union(df5.index)).interpolate()
df52.head()


# In[33]:


df53 = df52.reindex(new_index)
df53.head()


# In[34]:


dfout = df53.dropna(how='any')


# In[35]:


dfout


# In[36]:


dfout.to_pickle("proj5_ex05.pkl")


# In[ ]:




