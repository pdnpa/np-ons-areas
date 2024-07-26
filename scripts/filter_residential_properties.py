import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm

def filter_and_clip_csv(input_csv, buffer_gdf, header):
    # Load the CSV file with the correct header
    df = pd.read_csv(input_csv, names=header)
    
    # Filter for residential properties
    df_residential = df[df['CLASS'] == 'R'] # subset residential
    
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df_residential,
        geometry=gpd.points_from_xy(df_residential['X_COORDINATE'], df_residential['Y_COORDINATE']),
        crs="EPSG:27700"  # Assuming the coordinates are in British National Grid
    )
    
    # Clip the GeoDataFrame to the buffer
    clipped_gdf = gpd.clip(gdf, buffer_gdf)
    
    return clipped_gdf

def main():
    input_dir = '../data/ABPOGB_CSV/data'
    header_path = '../data/ABPOGB_CSV/resources/AddressBase_Header.csv'
    buffer_path = '../data/National_Parks_Buffer.shp'
    temp_dir = '../data/ABPOGB_CSV/temp'
    
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Load the header
    header = pd.read_csv(header_path).columns.tolist()
    print("Header loaded successfully.")
    
    # Load the buffer shapefile
    buffer_gdf = gpd.read_file(buffer_path)
    print("Buffer shapefile loaded successfully.")
    
    # Process each CSV file
    csv_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    for csv_file in tqdm(csv_files, desc="Processing CSV files"):
        clipped_gdf = filter_and_clip_csv(csv_file, buffer_gdf, header)
        
        # Save the clipped GeoDataFrame to a temporary shapefile
        output_file = os.path.join(temp_dir, os.path.basename(csv_file).replace('.csv', '.shp'))
        clipped_gdf.to_file(output_file)
    
    print("All CSV files processed and clipped successfully.")

if __name__ == "__main__":
    main()
