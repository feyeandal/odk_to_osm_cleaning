import os
import pandas as pd

def capitalize(fieldval):
    fieldval = str(fieldval)
    roman_letters = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    vals = fieldval.split(' ') # split field string by whitespace
    outval = []
    for val in vals:
        if val in roman_letters:
            outval.append(val)
        else:
            outval.append(val.title())
    return ' '.join(outval)

def foo(directory, out_path):
    # Create folder inside output folder
    folder = os.path.basename(directory) # Returns 10222020 etc
    output_folder = os.path.join(out_path, folder)
    print(output_folder)
    try:
        os.mkdir(output_folder)
    except Exception as e:
        print(e)

    # Iterate on each CSV file downloaded from the server
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(filename)
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            # Delete unnecessary tags
            df.drop(['survey_date_today','geopoint.altitude','geopoint.precision','meta.instanceId','meta.instanceName', 
            'meta.formId','meta.deviceId','meta.submissionTime'], axis=1, inplace=True, errors='ignore')

            # Delete duplicate tags from multiple choice questions
            df.drop(df.filter(regex='/').columns, axis=1, inplace=True)

            # Rename columns to OSM readable tags
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

            # Force building level values to integer type
            int_col = ['building:levels']
            for inte in int_col:
                if inte in renamed_df.columns:
                    renamed_df[inte] = renamed_df[inte].replace(' ','NaN', regex=True)
                    renamed_df[inte] = pd.to_numeric(renamed_df[inte], errors='coerce').astype('Int64')

            # Replace whitespace with semi-colon on multiple selection values
            col_names = ['building:material', 'floor:material', 'roof:material', 'healthcare']
            for col in col_names:
                if col in renamed_df.columns:
                    renamed_df[col] = renamed_df[col].replace(' ', ';', regex=True)

            # Capitalize first letter of each word
            title_col = ['addr:street', 'name', 'operator']
            for title in title_col:
                if title in renamed_df.columns:
                    capitalizer = lambda x: capitalize(x)
                    renamed_df[title] = renamed_df[title].apply(capitalizer)
            

            # Write to a CSV file using output_folder
            renamed_df.to_csv(os.path.join(output_folder, filename), index=None)

if __name__ == '__main__': 
    # directory = r'C:\Users\andal\Documents\GIS\odk_cleaner\new'
    base_dir = os.path.dirname(os.path.abspath('__file__')) # Get the current location of the file as the base path
    out_path = os.path.join(base_dir, 'output')
    input_path = os.path.join(base_dir, 'input')

    # Try to create overall output folder
    try:
        os.mkdir(out_path)
    except Exception as e:
        print(e)

    folders = os.listdir(input_path)
    map_dir_to_folder = lambda x: os.path.join(input_path, x) # Function to join directory with specific folder
    directories = map(map_dir_to_folder, folders) # Apply that function to the folders list. Read on python map and lambda
    for path in directories:
        print(path, out_path)
        foo(path, out_path)
