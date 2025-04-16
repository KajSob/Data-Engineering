#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import numpy as np


# In[2]:


df = pd.read_csv('proj1_ex01.csv')


# In[3]:


dict_array = []
for col in df.columns:
    typ = df[col].dtype
    if typ == "int64":
        typ = "int"
    elif typ == "float64":
        typ = "float"
    else:
        typ = "other"
    dict = { 
        "name": df[col].name,
        "missing": df[col].isnull().mean(),
        "type": typ
    }
    dict_array.append(dict)
print(dict_array)


# In[4]:


with open("proj1_ex01_fields.json", "w") as f: 
    json.dump(dict_array, f)


# In[5]:


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)


# In[6]:


big_dict = {}
for col in df.columns:
    if df[col].dtype == "int64" or df[col].dtype == "float64":
        small_dict = {
            "count": df[col].describe()["count"],
            "mean": df[col].describe()["mean"],
            "std": df[col].describe()["std"],
            "min": df[col].describe()["min"],
            "25%": df[col].describe()["25%"],
            "50%": df[col].describe()["50%"],
            "75%": df[col].describe()["75%"],
            "max": df[col].describe()["max"],
        }
    else:
        small_dict = {
            "count": df[col].describe(include="all")["count"],
            "unique": df[col].describe(include="all")["unique"],
            "top": df[col].describe(include="all")["top"],
            "freq": df[col].describe(include="all")["freq"],
        }
    big_dict[df[col].name] = small_dict
print(big_dict)


# In[7]:


with open("proj1_ex02_stats.json", "w") as f: 
    json.dump(big_dict, f,cls=NumpyEncoder)


# In[8]:


df.columns


# In[9]:


done = {}
for col in df.columns:
    new = ''
    for c in col:
        if c.isalnum() or c == ' ' or c == '_':
            if c == ' ':
                c = '_'
            new= new + c.lower()
        
    done[col] = new

df = df.rename(columns=done)


# In[10]:


df


# In[11]:


df.to_csv("proj1_ex03_columns.csv", index=False)


# In[12]:


df.to_excel("proj1_ex04_excel.xlsx", index=False)

df.to_json("proj1_ex04_json.json", orient="records")

df.to_pickle("proj1_ex04_pickle.pkl")


# In[13]:


pe = pd.read_pickle("proj1_ex05.pkl")


# In[14]:


pe


# In[15]:


list = []
for i in pe.index:
    if i.startswith('v'):
        list.append(i)
pe2 = pe.iloc[:,[1,2]]
pe3 = pe2.loc[list]


# In[16]:


with open("proj1_ex05_table.md", "w") as f:
    f.write(pe3.fillna("").to_markdown())


# In[17]:


with open("proj1_ex06.json", "r") as file:
    data = json.load(file)

ja = pd.json_normalize(data, sep='.')


# In[18]:


ja


# In[19]:


ja.to_pickle("proj1_ex06_pickle.pkl")


# In[ ]:




