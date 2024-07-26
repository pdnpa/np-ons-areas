# National Parks Address Processing

This repository contains scripts for processing address data within National Parks in England. The scripts perform the following tasks:

1. Clip address data to the boundaries of National Parks.
2. Filter residential addresses and combine them into a single shapefile.
3. Calculate population and address statistics for output areas intersecting National Parks.

## Directory Structure

```plaintext
.
├── data
│   ├── ABPOGB_CSV
│   ├── AddressBasePremium
│   ├── National_Parks_Buffer.shp
│   ├── National_Parks_(England)___Natural_England.shp
│   ├── OA_2021.shp
│   ├── oa_age_bands.csv
│   └── Output_Areas_2021
├── scripts
│   ├── clip_address_base.py
│   ├── filter_residential_properties.py
│   └── output_area_population.py
├── README.md
```

## Data Sources
* Output Areas (December 2021) Boundaries EW BFC (V8) Date updated 05/31/2024 | 2021, ONS Geography Open Data
* TS007A - Age by five-year age bands Total, ONS Crown Copyright Reserved [from Nomis on 26 July 2024] | | Office for National Statistics 
* National Parks (England), June 18th 2024 | Natural England Open Data Publication
* AddressBase | 0Ordnance Survey Digital Data
* National park residents, England and Wales: Census 2021 | Office for National Statistics 

## Requirements
* Python 3.9
* pandas library
* geopandas library
* shapely library
* tqdm library

## Scripts

### 1. clip_address_base.py
This script clips the AddressBasePremium data to the boundaries of National Parks.
* Loads the National Parks buffer shapefile.
* Reads the AddressBasePremium data in chunks.
* Clips each chunk to the National Parks boundaries.
* Saves the clipped data as temporary shapefiles.

### 2. filter_residential_properties.py
This script filters residential properties from the AddressBasePremium data and combines them into a single shapefile.
* Loads the clipped shapefiles from the previous step.
* Filters residential properties based on the CLASS column.
* Combines the filtered data into a single GeoDataFrame.
* Exports the combined residential addresses to a shapefile.

### 3. output_area_population.py
This script calculates population and address statistics for output areas intersecting National Parks.
* Loads the Output Areas shapefile, population CSV, National Parks shapefile, and residential addresses shapefile.
* Clips the Output Areas shapefile to the National Parks boundaries.
* Adds the name of the National Park to each Output Area.
* Merges population data with the clipped Output Areas.
* Counts the number of residential addresses inside and outside the National Parks for each Output Area.
* Exports the final data to a shapefile.
