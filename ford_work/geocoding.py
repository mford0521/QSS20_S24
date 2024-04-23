
import csv
import pandas as pd
import googlemaps

# load data, access google api key
# removed key to avoid rerunning and paying (only certain number of calls are free)
gmaps_key = googlemaps.Client(key="")
data = pd.read_csv('my_work/psets/pset2/jobs.csv')
df = data.copy()
df = df[["EMPLOYER_ADDRESS_1", "EMPLOYER_ADDRESS_2",	"EMPLOYER_CITY","EMPLOYER_STATE",	"EMPLOYER_POSTAL_CODE"]]
df = df.drop_duplicates()

# concatenate addresses
df['Address'] = df.apply(lambda x: ' '.join(filter(None, [str(x['EMPLOYER_ADDRESS_1']),  
                                                          str(x['EMPLOYER_CITY']), 
                                                          str(x['EMPLOYER_STATE']), 
                                                          str(x['EMPLOYER_POSTAL_CODE'])])), axis=1)

print(df['Address'].head())

# function to turn address into geocoded location
def geocode(add):
    g = gmaps_key.geocode(add)
    if g:
        lat = g[0]["geometry"]["location"]["lat"]
        lng = g[0]["geometry"]["location"]["lng"]
        return (lat, lng)
    else:
        return None

# apply function on column and add columns to csvs 
df['geocoded'] = df['Address'].apply(geocode)
print(df['geocoded'].head())
data['geocoded'] = df['geocoded']

# export csvs
data.to_csv('my_work/psets/pset2/full_jobs.csv', index=False)
df.to_csv('my_work/psets/pset2/address_jobs.csv', index=False)

