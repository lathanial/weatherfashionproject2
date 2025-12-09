import json
from pathlib import Path
from datetime import datetime, timedelta
import random

# Directories
output_dir = Path("data/raw/noaa")
output_dir.mkdir(parents=True, exist_ok=True)

# Cities
metro_areas = [
    "New York", "Los Angeles", "Chicago", "Houston",
    "Phoenix", "Philadelphia", "San Antonio", "San Diego"
]

# Date range
start_date = datetime(2013, 1, 1)
end_date = datetime(2013, 1, 10)  # short range for testing, extend as needed
delta = timedelta(days=1)

# Datatypes
datatypes = ["TMAX", "TMIN", "PRCP", "SNOW", "AWND"]

# Generate mock data
for city in metro_areas:
    city_data = []
    current_date = start_date
    while current_date <= end_date:
        for dt in datatypes:
            value = round(random.uniform(0, 30), 1) if dt in ["TMAX", "TMIN"] else round(random.uniform(0, 10), 1)
            city_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "datatype": dt,
                "value": value
            })
        current_date += delta
    
    # Save as JSON
    filename = f"{city.lower().replace(' ', '_')}_weather.json"
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        json.dump(city_data, f, indent=2)
    
    print(f"✓ Mock NOAA data saved: {filepath}")

# Save a small metadata file
metadata = {
    "collection_date": datetime.now().isoformat(),
    "cities": metro_areas,
    "datatypes": datatypes,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d")
}

with open(output_dir / "collection_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Metadata saved: {output_dir / 'collection_metadata.json'}")