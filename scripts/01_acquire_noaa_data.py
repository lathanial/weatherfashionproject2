import requests
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

NOAA_API_TOKEN = "slCkptMeMNzVgHEgAMpYBLYTWNTGUVZH"
NOAA_BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

output_dir = Path("data/raw/noaa")
output_dir.mkdir(parents=True, exist_ok=True)

cities = {
    "New York": "GHCND:USW00094728",
    "Los Angeles": "GHCND:USW00023174",
    "Chicago": "GHCND:USW00094846",
    "Houston": "GHCND:USW00012960",
    "Phoenix": "GHCND:USW00023183",
    "Philadelphia": "GHCND:USW00013739",
    "San Antonio": "GHCND:USW00012921",
    "San Diego": "GHCND:USW00023188"
}

datatypes = ["TMAX", "TMIN", "PRCP", "SNOW", "AWND"]

start_date = "2013-01-01"
end_date = "2022-12-31"

def calculate_checksum(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def fetch_noaa_data(station_id, start, end, datatypes_list):
    headers = {"token": NOAA_API_TOKEN}
    
    params = {
        "datasetid": "GHCND",
        "stationid": station_id,
        "startdate": start,
        "enddate": end,
        "datatypeid": ",".join(datatypes_list),
        "units": "metric",
        "limit": 1000
    }
    
    all_data = []
    offset = 1
    
    while True:
        params["offset"] = offset
        
        try:
            print(f"  requesting offset {offset}...")
            response = requests.get(NOAA_BASE_URL, headers=headers, params=params)
            
            time.sleep(0.25)
            
            if response.status_code == 200:
                data = response.json()
                
                if "results" not in data or len(data["results"]) == 0:
                    break
                
                all_data.extend(data["results"])
                
                if len(data["results"]) < 1000:
                    break
                
                offset += 1000
                
            elif response.status_code == 429:
                print("  rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                continue
                
            else:
                print(f"  error: {response.status_code}")
                print(f"  response: {response.text}")
                break
                
        except Exception as e:
            print(f"  exception: {e}")
            break
    
    return all_data

def process_noaa_data(raw_data, city_name):
    processed = []
    
    for record in raw_data:
        processed.append({
            "city": city_name,
            "date": record.get("date", ""),
            "datatype": record.get("datatype", ""),
            "value": record.get("value", None),
            "attributes": record.get("attributes", "")
        })
    
    return processed

print("starting noaa data acquisition...")
print(f"date range: {start_date} to {end_date}")
print(f"cities: {len(cities)}")
print(f"datatypes: {', '.join(datatypes)}")
print()

metadata = {
    "collection_date": datetime.now().isoformat(),
    "date_range": {
        "start": start_date,
        "end": end_date
    },
    "datatypes": datatypes,
    "cities": list(cities.keys()),
    "stations": cities
}

for city_name, station_id in cities.items():
    print(f"fetching data for {city_name} (station: {station_id})...")
    
    all_city_data = []
    
    for year in range(2013, 2023):
        year_start = f"{year}-01-01"
        year_end = f"{year}-12-31"
        
        print(f"  fetching year {year}...")
        year_data = fetch_noaa_data(station_id, year_start, year_end, datatypes)
        
        if year_data:
            all_city_data.extend(year_data)
            print(f"    got {len(year_data)} records")
    
    if all_city_data:
        processed_data = process_noaa_data(all_city_data, city_name)
        
        filename = f"{city_name.lower().replace(' ', '_')}_weather.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(processed_data, f, indent=2)
        
        print(f"  saved {len(processed_data)} records to {filepath}")
        
        checksum = calculate_checksum(filepath)
        checksum_file = output_dir / f"{filename}.sha256"
        with open(checksum_file, 'w') as f:
            f.write(f"{checksum}  {filename}\n")
        
        print(f"  checksum saved to {checksum_file}")
    else:
        print(f"  no data retrieved for {city_name}")
    
    print()

metadata_file = output_dir / "collection_metadata.json"
with open(metadata_file, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"metadata saved to {metadata_file}")
print("done!")