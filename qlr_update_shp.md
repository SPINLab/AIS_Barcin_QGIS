Create qlr files from locus layer based on shpname. Before you do this make sure to have the [AAAA.qlr]() file store in a new folder QLR in your project folder. (e.g. C:\Barcin\QLR\AAAA.qlr)

```python
import geopandas as gpd

loc_output = input("Fill in path where the OUTPUT folder is in:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")

poly_path = loc_output+'OUTPUT\\BH_locus.shp'


# Read in the shapefile as a GeoDataFrame
locus_gdf = gpd.read_file(poly_path)

# Get the unique values of the 'plan' and 'trench' fields
unique_shape = locus_gdf['shpname'].unique()
unique_shape = [s.replace("_locus", "") for s in unique_shape]

import os
# define the input file path
input_file = loc_output+"QLR\AAAA.qlr"

# define the list of replacements
replacements = unique_shape

# loop through the list of replacements and replace the values in the input file
for replacement in replacements:
    # create the new file name
    new_file_name = replacement + ".qlr"

    # define the output file path
    output_file = os.path.join(os.path.dirname(input_file), new_file_name)

    # read the input file and replace the AAAA and BBBB values
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # replace AAAA and BBBB with the values from the current replacement
            line = line.replace("AAAA", replacement).replace("G:/Barcin_Project/", loc_output)

            # write the modified line to the output file
            f_out.write(line)

    # print the name of the new file
    print("Created file:", output_file)
```
