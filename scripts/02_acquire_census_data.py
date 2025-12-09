import requests
import pandas as pd
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

CENSUS_API_KEY = "91818ac7fca0c187d5dc255d0795348993346e2b"
MRTS_BASE_URL = "https://api.census.gov/data/timeseries/eits/mrts"
ARTS_BASE_URL = "https://api.census.gov/data"

output_dir = Path("data/raw/census")
output_dir.mkdir(parents=True, exist_ok=True)

naics_codes = {
    "4481": "Clothing Stores",
    "44811": "Men's Clothing Stores",
    "44812": "Women's Clothing Stores",
    "44813": "Children's Clothing Stores",
    "44814": "Family Clothing Stores",
    "44815": "Clothing Accessories Stores",
    "4482": "Shoe Stores",
    "4483": "Jewelry and Luggage Stores"
}

start_year = 2013
end_year = 2022

state_codes = {
    "36": "New York",
    "06": "California",
    "17": "Illinois",
    "48": "Texas",
    "04": "Arizona",
    "42": "Pennsylvania"
}

def calculate_checksum(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def fetch_mrts_data(year):
    params = {
        "get": "cell_value,data_type_code,time_slot_id,category_code",
        "time": year,
        "key": CENSUS_API_KEY
    }
    
    try:
        print(f"  requesting MRTS data for year {year}...")
        response = requests.get(MRTS_BASE_URL, params=params)
        
        time.sleep(0.5)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                return data
            else:
                print(f"    no data returned")
                return None
        else:
            print(f"    error: {response.status_code}")
            print(f"    response: {response.text}")
            return None
            
    except Exception as e:
        print(f"    exception: {e}")
        return None

def fetch_arts_data(year):
    url = f"{ARTS_BASE_URL}/{year}/abstcb"
    
    params = {
        "get": "NAICS2017,NAICS2017_TTL,ESTAB,RCPTOT,PAYANN",
        "for": "state:*",
        "NAICS2017": "4481",
        "key": CENSUS_API_KEY
    }
    
    try:
        print(f"  requesting ARTS data for year {year}...")
        response = requests.get(url, params=params)
        
        time.sleep(0.5)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                return data
            else:
                print(f"    no data returned")
                return None
        else:
            print(f"    error: {response.status_code}")
            print(f"    response: {response.text}")
            return None
            
    except Exception as e:
        print(f"    exception: {e}")
        return None

print("starting census data acquisition...")
print(f"years: {start_year} to {end_year}")
print(f"naics codes: {len(naics_codes)}")
print()

metadata = {
    "collection_date": datetime.now().isoformat(),
    "date_range": {
        "start": start_year,
        "end": end_year
    },
    "naics_codes": naics_codes,
    "monthly_records": 0,
    "annual_records": 0
}

print("fetching monthly retail trade survey (mrts) data...")
monthly_data = []

for year in range(start_year, end_year + 1):
    data = fetch_mrts_data(year)
    
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])
        df['year'] = year
        df['frequency'] = 'monthly'
        monthly_data.append(df)
        
        print(f"    added {len(df)} records")

if monthly_data:
    monthly_df = pd.concat(monthly_data, ignore_index=True)
    monthly_file = output_dir / "monthly_retail_sales.csv"
    monthly_df.to_csv(monthly_file, index=False)
    
    print(f"saved {len(monthly_df)} monthly records to {monthly_file}")
    
    checksum = calculate_checksum(monthly_file)
    checksum_file = output_dir / "monthly_retail_sales.csv.sha256"
    with open(checksum_file, 'w') as f:
        f.write(f"{checksum}  monthly_retail_sales.csv\n")
    
    metadata["monthly_records"] = len(monthly_df)
else:
    print("no monthly data retrieved")

print()

metadata_file = output_dir / "collection_metadata.json"
with open(metadata_file, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"metadata saved to {metadata_file}")
print("done!")