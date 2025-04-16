#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import numpy as np
import json
import geopandas as gpd
import pyrosm
from shapely.ops import linemerge
import pickle
import contextily as cx
import matplotlib.pyplot as plt


# In[26]:


f = open('proj4_params.json')
params = json.load(f)
f.close()
params


# In[27]:


gdf = gpd.read_file("proj4_points.geojson")
gdf = gdf.to_crs('epsg:2180')


# In[28]:


gdf.crs


# In[29]:


gdf


# In[30]:


gdf.sindex.valid_query_predicates


# In[31]:


gdf_ill = gdf.copy()
gdf_ill['geometry']= gdf.buffer(100)
gdf_ill


# In[32]:


bomba = gpd.sjoin(gdf, gdf_ill, predicate='intersects')
bomba


# In[33]:


df_count = pd.DataFrame(bomba[f"{params['id_column']}_left"].value_counts(sort=True))
df_count = df_count.rename_axis(params["id_column"],axis=0)
df_count.to_csv("proj4_ex01_counts.csv")
df_count


# In[34]:


latlon = gdf[[params['id_column'], 'geometry']]
latlon = latlon.to_crs(epsg=4326)
print(latlon.geometry)
latlon['lat'] = latlon.geometry.y.round(7)
latlon['lon'] = latlon.geometry.x.round(7)
latlon = latlon.drop(columns=['geometry'])
latlon.to_csv('proj4_ex01_coords.csv', index=False)
latlon


# In[35]:


pyr = pyrosm.get_data(params['city'])
osm = pyrosm.OSM(pyr)
road = osm.get_network(network_type="driving")
road


# In[36]:


out =[]
for i in road.index:
    if road.loc[i]['highway'] != 'tertiary':
        out.append(i)


# In[37]:


road = road.drop(out)
road


# In[38]:


def to_line(ryba):
    if ryba.geom_type == 'MultiLineString':
        return linemerge(ryba)
    else:
        return ryba
road['geometry'] = road['geometry'].apply(to_line)


# In[39]:


road.explore()


# In[16]:


rs = road[['id','name','geometry']].copy()
rs = rs.rename(columns={'id':'osm_id'})
rs.to_file('proj4_ex02_roads.geojson', driver='GeoJSON')  
rs.explore()
rs.crs


# In[17]:


rs.to_crs('epsg:2180', inplace=True)
bang = rs.copy()
bang.to_crs('epsg:2180', inplace=True)
bang['geometry']= rs.geometry.buffer(50,cap_style=2)
bang.to_crs('epsg:2180', inplace=True)
bang.explore()


# In[18]:


gamba = gpd.sjoin(bang, gdf, predicate='intersects')
gamba


# In[19]:


lisz = pd.DataFrame(gamba["name"].value_counts(sort=True))
lisz = lisz.sort_index()
lisz.to_csv('proj4_ex03_streets_points.csv')
lisz


# In[20]:


pol= gpd.read_file("proj4_countries.geojson")
pol


# In[21]:


ez = pol.boundary
ez


# In[22]:


ez.explore()


# In[23]:


with open('proj4_ex04_gdf.pkl', 'wb') as f:
    pickle.dump(ez, f)


# In[41]:


for i in pol.index:
    dodo = gpd.GeoDataFrame({'geometry':[ez.loc[i]]})
    dodo.set_crs('epsg:3857', inplace=True)
    ax = dodo.plot()
    print(cx.add_basemap(ax, crs=ez.crs.to_string(),source=cx.providers.OpenStreetMap.Mapnik))
    plt.savefig(f"proj4_ex04_{pol.loc[i]['name'].lower()}.png")


# In[ ]:




