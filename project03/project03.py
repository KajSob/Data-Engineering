#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
from pandas.api.types import is_numeric_dtype


# In[2]:


df = pd.concat([pd.read_json("proj3_data1.json"),pd.read_json("proj3_data2.json"),pd.read_json("proj3_data3.json")], ignore_index = True)
df


# In[3]:


df.to_json("proj3_ex01_all_data.json") 


# In[4]:


df_miss = pd.DataFrame({"col":[],"val":[]})
for col in df.columns:
    if pd.isnull(df[col]).sum()!=0:
        df_miss.loc[len(df_miss.index)] = [col, pd.isnull(df[col]).sum()]


# In[5]:


df_miss


# In[6]:


df_miss.to_csv("proj3_ex02_no_nulls.csv",header=False,index=False)


# In[7]:


f = open('proj3_params.json')
params = json.load(f)
f.close()
params


# In[8]:


desc_list = []
for row in df.index:
    desc_small = ""
    for col in params["concat_columns"]:
        if desc_small == "":
            desc_small = df.loc[row][col]
        else:
            desc_small= desc_small +" "+ df.loc[row][col]
    desc_list.append(desc_small)
df = df.assign(description=desc_list)
df


# In[9]:


df.to_json("proj3_ex03_descriptions.json")


# In[10]:


df_more = pd.read_json("proj3_more_data.json")


# In[11]:


df_more


# In[12]:


df_big = df.merge(df_more,on=params["join_column"],how="left")
df_big.to_json("proj3_ex04_joined.json")


# In[13]:


df_less = df_big.copy().drop(columns='description')
for row in df_less.index:
    name = df_big["description"][row]
    name = name.lower().replace(' ','_')
    name = f"proj3_ex05_{name}.json"
    df_less.loc[row].to_json(name)


# In[14]:


for col in params["int_columns"]:
    df_less[col]=df_less[col].astype('Int64')


# In[15]:


for row in df_less.index:
    name = df_big["description"][row]
    name = name.lower().replace(' ','_')
    name = f"proj3_ex05_int_{name}.json"
    df_less.loc[row].to_json(name)


# In[16]:


agg_dict = {}
for agg in params["aggregations"]:
    agg_dict[f"{agg[1]}_{agg[0]}"]=df_big[agg[0]].aggregate(func=agg[1])
agg_dict


# In[17]:


with open("proj3_ex06_aggregations.json", "w") as outfile: 
    json.dump(agg_dict, outfile)


# In[18]:


df_big


# In[19]:


df_gr = df_big.copy()
for col in df_big.columns:
    if (not is_numeric_dtype(df_big[col])) and (col != params["grouping_column"]):
        df_gr = df_gr.drop(columns=col)
df_gr


# In[20]:


counter = {}
for row in df_gr[params["grouping_column"]]:
    if row in counter:
        counter[row] += 1
    else:
        counter[row] = 1
counter


# In[21]:


df_group = df_gr.groupby([params["grouping_column"]]).mean()
for row in counter:
    if counter[row] <=1:
        df_group = df_group.drop(index=row)
df_group


# In[22]:


df_group.to_csv("proj3_ex07_groups.csv",header=True,index=True)


# In[23]:


df_order = df_big.pivot_table(aggfunc='max',index=params["pivot_index"], columns = params["pivot_columns"], values = params["pivot_values"])
df_order


# In[24]:


df_order.to_pickle("proj3_ex08_pivot.pkl")


# In[25]:


df_longer = df_big.melt(params["id_vars"])
df_longer


# In[26]:


df_longer.to_csv("proj3_ex08_melt.csv",header=True,index=False)


# In[27]:


df_gamble = pd.read_csv("proj3_statistics.csv")
df_gamble = pd.wide_to_long(df_gamble,stubnames=df_big[params["pivot_index"]].unique(),i=df_gamble.columns[0],j='yr', sep="_",suffix="\d+")
for col in df_gamble:
    if all(np.isnan(var) for var in df_gamble[col]):
        df_gamble = df_gamble.drop(columns=col)
df_gamble = df_gamble.rename_axis([None,None],axis=0)
idx_list =[]
for idx in df_gamble.index:
    idx_list.append(str(idx))

df_gamble = df_gamble.reset_index()
df_gamble.index = idx_list

df_gamble = df_gamble.drop(columns=[df_gamble.columns[0],df_gamble.columns[1]])
df_gamble


# In[28]:


df_gamble.to_pickle('proj3_ex08_stats.pkl')


# In[29]:


#ostatnie tylko do poprawy, wybrac new albo gamble

