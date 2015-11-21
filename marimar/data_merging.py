
import pandas as pd
import numpy as np
import geocoder as gc
df = pd.read_csv('hospitalList_processed.csv')
no_lat_lon = df[(df.lat <= 0.0) & (df.lon <= 0.0)]
complete = df[~((df.lat <= 0.0) & (df.lon <= 0.0))]

for index, row in no_lat_lon.iterrows():
    try:
        g = gc.google(row['Barangay Name'])
        no_lat_lon.set_value(index, 'lat', g.latlng[0])
        no_lat_lon.set_value(index, 'lon', g.latlng[1])
    except: # evil I know
        continue

complete = complete.append( no_lat_lon[~((no_lat_lon.lat <= 0.0) & (no_lat_lon.lon <= 0.0))])
missing = no_lat_lon[(no_lat_lon.lat <= 0.0) & (no_lat_lon.lon <= 0.0)]
missing.to_csv("missing_lat_lon.csv", index=False)

# DO HIV HOSPITALS
# Service Capabilities
service = pd.read_csv("serviceCapability.csv")
hospital_with_service = complete.merge(service, on="Facility Name" , how="left")
hospital_with_service.drop(["Unnamed: 0", "Province_x", "Province_y", "Region_x", "Region_y"], axis=1, inplace=True)
