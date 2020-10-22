import os
import pandas as pd

directory = 'C:\\Users\\andal\\Documents\\GIS\\odk_cleaner\\new'

# Iterate on each CSV file downloaded from the server and rename the columns to OSM readable keys
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(filename)
        renamed_df=df.rename(columns=({
        'addr_town' : 'addr:town',
        'social_facility_for' : 'social_facility:for',
        'addr_street' : 'addr:street',
        'capacity_persons' : 'capacity:persons',
        'building_levels' : 'building:levels',
        'building_material' : 'building:material',
        'floor_material' : 'floor:material',
        'survey_name' : 'survey:name',
        'survey_date' : 'survey:date',
        'emergency_amenity' : 'emergency:amenity',
        'emergency_social_facility' : 'emergency:social_facility',
        'emergency_social_facility_for' : 'emergency:social_facility:for',
        'emergency_hazard_type' : 'emergency:hazard_type',
        'isced_level' : 'isced:level',
        'townhall_type' : 'townhall:type',
        'operator_type' : 'operator:type',
        'roof_material' : 'roof:material',
        'kitchen_facilities' : 'kitchen:facilities',
        'capacity_pump' : 'capacity:pump',
        'generator_output_electricity' : 'generator:output:electricity',
        'generator_method' : 'generator:method',
        'generator_source' : 'generator:source',
        'plant_source' : 'plant:source',
        'geopoint.latitude' : 'latitude',
        'geopoint.longitude' : 'longitude'
        }))

        # Delete unnecessary tags
        renamed_df.drop(['survey_date_today','geopoint.altitude','geopoint.precision','meta.instanceId','meta.instanceName', 
        'meta.formId','meta.deviceId','meta.submissionTime'], axis=1, inplace=True, errors='ignore')

        # Delete duplicate tags from multiple choice questions
        renamed_df.drop(renamed_df.filter(regex='/').columns, axis=1, inplace=True)

        # Replace unnecessary values for building level
        renamed_df['building:levels'] = renamed_df['building:levels'].replace(' ','NaN', regex=True)
        renamed_df['building:levels'] = pd.to_numeric(renamed_df['building:levels'], errors='coerce').astype('Int64')

        # Replace whitespace with semi-colon on multiple selection values
        if 'building:material' in renamed_df.columns:
            renamed_df['building:material'] = renamed_df['building:material'].replace(' ',';', regex=True)       
        if 'floor:material' in renamed_df.columns:
            renamed_df['floor:material'] = renamed_df['floor:material'].replace(' ',';', regex=True)  
        if 'roof:material' in renamed_df.columns:
            renamed_df['roof:material'] = renamed_df['roof:material'].replace(' ',';', regex=True) 
        if 'healthcare' in renamed_df.columns:
            renamed_df['healthcare'] = renamed_df['healthcare'].replace(' ',';', regex=True)

        # Convert values to proper names
        if 'addr:street' in renamed_df.columns:
            renamed_df['addr:street'] = renamed_df['addr:street'].str.title()
        if 'name' in renamed_df.columns:
            renamed_df['name'] = renamed_df['name'].str.title()
        if 'operator' in renamed_df.columns:
            renamed_df['operator'] = renamed_df['operator'].str.title()

        # Write to a CSV file
        renamed_df.to_csv('output/' + filename, index=None)