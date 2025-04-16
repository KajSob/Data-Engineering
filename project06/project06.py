#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sqlite3


# In[2]:


con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()
result = cur.execute("SELECT count(*) from readings;").fetchall()
df = pd.DataFrame(result)
df


# In[10]:


result = cur.execute("SELECT count(DISTINCT detector_id) from readings;").fetchall()
df1 = pd.DataFrame(result)
df1


# In[11]:


df1.to_pickle("proj6_ex01_detector_no.pkl")


# In[14]:


result = cur.execute("SELECT detector_id, count(count),min(starttime),max(starttime) from readings GROUP BY detector_id;").fetchall()
df2 = pd.DataFrame(result)
df2


# In[16]:


df2.to_pickle("proj6_ex02_detector_stat.pkl")


# In[28]:


result = cur.execute("SELECT detector_id, count, LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) from readings WHERE detector_id is 146 LIMIT 500;").fetchall()
df3 = pd.DataFrame(result)
df3


# In[29]:


df3.to_pickle("proj6_ex03_detector_146_lag.pkl")


# In[38]:


result = cur.execute("SELECT detector_id, count, SUM(count) OVER (PARTITION BY detector_id ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) from readings WHERE detector_id is 146 LIMIT 500;").fetchall()
df4 = pd.DataFrame(result)
df4


# In[39]:


df4.to_pickle("proj6_ex04_detector_146_sum.pkl")


# In[ ]:




