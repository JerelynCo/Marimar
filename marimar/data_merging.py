
import pandas as pd
import numpy as np
import geocoder as gc
df = pd.read_csv('hospitalList_processed.csv')
no_lat_lon = df[(df.lat <= 0.0) & (df.lon <= 0.0)]

for index, row in no_lat_lon.iterrows():
    try:
        g = gc.google(row['Barangay Name'])
        no_lat_lon.set_value(index, 'lat', g.latlng[0])
        no_lat_lon.set_value(index, 'lon', g.latlng[1])
    except: # evil I know 
        continue
