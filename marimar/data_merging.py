
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

# Service Capabilities
service = pd.read_csv("serviceCapability.csv")
hospital_with_service = complete.merge(service, on="Facility Name" , how="left")
hospital_with_service.drop(["Unnamed: 0", "Province_x", "Province_y", "Region_x", "Region_y"], axis=1, inplace=True)

hospitals = pd.read_csv('hospitals_with_service.csv')
faci = pd.read_csv('filters.csv')
hospitals_with_facilities = pd.merge(hospitals, faci, on="level", how="outer")

# DO HIV HOSPITALS
treat = pd.read_csv("hiv_treatment_centers.csv")
treat = treat[treat["region "] == "NCR"]
treat.drop(["region ", "address", "hact_chair", "lon", "lat", "contact_number", "Unnamed: 0"], axis=1, inplace=True)
treat["HIVTreat"] = 1
treat.treatment_hub = treat.treatment_hub.map(lambda x: x.upper())
hospitals = hospitals.merge(treat, how="outer", left_on="Facility Name", right_on="treatment_hub")

test.drop(['Unnamed: 0', 'address', 'telephone_number', 'lon', 'lat'], axis=1, inplace=True)
test['reffering_unit_or_laboratories'] = test['reffering_unit_or_laboratories'].map(lambda x: x.upper())
test['HIVTest'] = 1
hospitals = hospitals.merge(test, how="outer", left_on="Facility Name", right_on='reffering_unit_or_laboratories')
