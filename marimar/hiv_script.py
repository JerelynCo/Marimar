import pandas as pd
import geocoder

hiv_testing_centers = pd.read_csv("data/doh_hiv_testing_hospitals_ncr.csv")


hiv_testing_centers['lon'] = 0.0
hiv_testing_centers['lat'] = 0.0
for i in hiv_testing_centers['address'].index:
	g = geocoder.google(hiv_testing_centers['address'][i] + ', PH')
	if g.geojson['properties']['ok'] == False:
		print(i, ': failed to locate')
		hiv_testing_centers['lon'][i] = 0.0
		hiv_testing_centers['lat'][i] = 0.0
	else:
		print(i, ': located')
		hiv_testing_centers['lon'][i] = g.geojson['geometry']['coordinates'][0]
		hiv_testing_centers['lat'][i] = g.geojson['geometry']['coordinates'][1]
	print(hiv_testing_centers['lon'][i])


hiv_treatment_centers = pd.read_csv("data/doh_treatment_hubs_for_people_living_with_hiv_including_pregnant_women.csv")
hiv_treatment_centers['lon'] = 0.0
hiv_treatment_centers['lat'] = 0.0

for i in hiv_treatment_centers['address'].index:
	g = geocoder.google(hiv_treatment_centers['address'][i] + ', PH')
	if g.geojson['properties']['ok'] == False:
		print(i, ': failed to locate')
		hiv_treatment_centers['lon'][i] = 0.0
		hiv_treatment_centers['lat'][i] = 0.0
	else:
		print(i, ': located')
		hiv_treatment_centers['lon'][i] = g.geojson['geometry']['coordinates'][0]
		hiv_treatment_centers['lat'][i] = g.geojson['geometry']['coordinates'][1]
	print(hiv_treatment_centers['lon'][i])


hygiene_centers = pd.read_csv("data/doh_social_hygiene_clinic.csv")
hygiene_centers['lon'] = 0.0
hygiene_centers['lat'] = 0.0

for i in hygiene_centers['address'].index:
	g = geocoder.google(hygiene_centers['address'][i] + ', PH')
	if g.geojson['properties']['ok'] == False:
		print(i, ': failed to locate')
		hygiene_centers['lon'][i] = 0.0
		hygiene_centers['lat'][i] = 0.0
	else:
		print(i, ': located')
		hygiene_centers['lon'][i] = g.geojson['geometry']['coordinates'][0]
		hygiene_centers['lat'][i] = g.geojson['geometry']['coordinates'][1]
	print(hygiene_centers['lon'][i])



hospitalList = pd.read_csv("HospitalList.csv")
hospitalList['lon'] = 0.0
hospitalList['lat'] = 0.0
for i in range(hospitalList.shape[0]):
	g = geocoder.google("%s, %s, %s, %s" %(hospitalList['Street Name and #'][i],hospitalList['Barangay Name'][i], hospitalList['City/Municipality'][i], "PH" ))

	if g.geojson['properties']['ok'] == False:
		print(i, ': failed to locate')
		hospitalList['lon'][i] = 0.0
		hospitalList['lat'][i] = 0.0
	else:
		print(i, ': located')
		hospitalList['lon'][i] = g.geojson['geometry']['coordinates'][0]
		hospitalList['lat'][i] = g.geojson['geometry']['coordinates'][1]
	
	print(hospitalList['lon'][i])
	print(hospitalList['lat'][i])
