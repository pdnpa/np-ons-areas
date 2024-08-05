import os
import pandas as pd
import geopandas as gpd
from tqdm import tqdm

def main():
    temp_dir = '../data/ABPOGB_CSV/temp'
    output_shapefile = '../data/residential_addresses.shp'
    
    # Load all temporary shapefiles
    print("Loading temporary shapefiles...")
    shapefiles = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.shp')]
    
    if not shapefiles:
        print("No temporary shapefiles found. Please ensure the filtering and clipping process completed successfully.")
        return
    
    # Combine all GeoDataFrames
    print("Combining GeoDataFrames...")
    gdfs = [gpd.read_file(f) for f in tqdm(shapefiles, desc="Reading temporary shapefiles")]
    combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
    print(f"Combined GeoDataFrame has {len(combined_gdf)} records.")
    
    if combined_gdf.empty:
        print("Combined GeoDataFrame is empty. Please check the filtering and clipping process for issues.")
        return
    
    # Export the combined GeoDataFrame to a Shapefile
    combined_gdf.to_file(output_shapefile, driver='ESRI Shapefile')
    print(f"Residential addresses have been exported to {output_shapefile}")

if __name__ == "__main__":
    main()
