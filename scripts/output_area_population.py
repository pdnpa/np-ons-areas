import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm

def main():
    oa_shapefile = '../data/Output_Areas_2021/OA_2021.shp'
    population_csv = '../data/oa_age_bands.csv'
    national_parks_shapefile = '../data/National_Parks_(England)___Natural_England.shp'
    residential_addresses_shapefile = '../data/residential_addresses.shp'
    
    # Load shapefiles and CSV
    print("Loading shapefiles and CSV...")
    oa_gdf = gpd.read_file(oa_shapefile)
    national_parks_gdf = gpd.read_file(national_parks_shapefile)
    population_df = pd.read_csv(population_csv)
    residential_addresses_gdf = gpd.read_file(residential_addresses_shapefile)
    
    # Ensure population CSV column names are consistent
    population_df.columns = ['OA21CD', 'Population']

    # Find intersection of OAs with National Parks
    print("Finding OAs that intersect with National Parks...")
    intersecting_oa_gdf = gpd.sjoin(oa_gdf, national_parks_gdf, how='inner', predicate='intersects')
    
    # Add the name of the National Park
    intersecting_oa_gdf['National_Park'] = intersecting_oa_gdf['NAME']
    
    # Drop duplicates to keep unique OAs
    intersecting_oa_gdf = intersecting_oa_gdf.drop_duplicates(subset='OA21CD')
    
    # Merge with population data
    print("Merging intersecting OA with population data...")
    intersecting_oa_gdf = intersecting_oa_gdf.merge(population_df, left_on='OA21CD', right_on='OA21CD', how='left')
    
    # Prepare to count addresses inside and outside National Parks
    print("Counting addresses inside and outside National Parks...")
    
    # Perform spatial join to count total addresses within OAs
    total_join = gpd.sjoin(residential_addresses_gdf, oa_gdf, how="inner", predicate='within')
    
    # Debugging: Print columns of total_join
    print("Columns in total_join after spatial join:", total_join.columns)
    
    # Ensure the column names match for grouping
    total_counts = total_join.groupby('OA21CD').size().reset_index(name='total_addresses')
    
    # Perform spatial join to count addresses inside National Parks
    inside_join = gpd.sjoin(residential_addresses_gdf, national_parks_gdf, how="inner", predicate='within')
    
    # Remove 'index_right' column if it exists
    if 'index_right' in inside_join.columns:
        inside_join = inside_join.drop(columns=['index_right'])
    
    # Perform spatial join to count addresses within intersecting OAs
    inside_join = gpd.sjoin(inside_join, intersecting_oa_gdf[['OA21CD', 'geometry']], how="inner", predicate='within')
    
    # Remove 'index_right' column if it exists
    if 'index_right' in inside_join.columns:
        inside_join = inside_join.drop(columns=['index_right'])
    
    # Debugging: Print columns of inside_join
    print("Columns in inside_join after spatial join:", inside_join.columns)
    
    # Ensure the column names match for grouping
    inside_counts = inside_join.groupby('OA21CD').size().reset_index(name='address_inside')
    
    # Merge the counts into the intersecting OA GeoDataFrame
    intersecting_oa_gdf = intersecting_oa_gdf.merge(inside_counts, on='OA21CD', how='left')
    intersecting_oa_gdf = intersecting_oa_gdf.merge(total_counts, on='OA21CD', how='left')
    
    # Calculate addresses outside by subtracting inside from total
    intersecting_oa_gdf['address_inside'] = intersecting_oa_gdf['address_inside'].fillna(0)
    intersecting_oa_gdf['total_addresses'] = intersecting_oa_gdf['total_addresses'].fillna(0)
    intersecting_oa_gdf['address_outside'] = intersecting_oa_gdf['total_addresses'] - intersecting_oa_gdf['address_inside']
    
    # Export the result to a new shapefile
    output_shapefile = '../data/output_area_population.shp'
    print(f"Exporting results to {output_shapefile}...")
    intersecting_oa_gdf.to_file(output_shapefile, driver='ESRI Shapefile')
    print("Script completed successfully!")

if __name__ == "__main__":
    main()





