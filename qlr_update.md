In order to create qlr files that have the data per layer seperated based on Trench and plan the following script has been created:

```python
import geopandas as gpd

# Step 1 set variables
loc_output = input("Fill in path where the OUTPUT folder is in:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")
poly_path = loc_ouput+'OUTPUT\\BH_locus.shp'

# Read in the shapefile as a GeoDataFrame
locus_gdf = gpd.read_file(poly_path)

# Get the unique values of the 'plan' and 'trench' fields
unique_plans = locus_gdf['Plan'].unique()
unique_trenches = locus_gdf['Trench'].unique()

# Create a list of all unique combinations of plan and trench
unique_combinations = []
for plan in unique_plans:
    for trench in unique_trenches:
        unique_combinations.append((plan, trench))

# Step2 replace numbers with 3 digit strings
for i, couple in enumerate(unique_combinations):
    num, text = couple
    if num.isdigit():
        num_str = num.zfill(3)
        unique_combinations[i] = (num_str, text)
 
# Step 3
# define the input file path
input_file = loc_output+"QLR\BH_TrenchAAAA_PlanBBBB.qlr"

# define the list of replacements
replacements = unique_combinations

# loop through the list of replacements and replace the values in the input file
for replacement in replacements:
    # get the AAAA and BBBB values from the current replacement
    aaa = replacement[1]
    bbb = replacement[0]

    # create the new file name
    new_file_name = "BH_Trench" + aaa + "_Plan" + bbb + ".qlr"

    # define the output file path
    output_file = os.path.join(os.path.dirname(input_file), new_file_name)

    # read the input file and replace the AAAA and BBBB values
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # replace AAAA and BBBB with the values from the current replacement
            line = line.replace("AAAA", aaa).replace("BBBB", bbb)

            # write the modified line to the output file
            f_out.write(line)

    # print the name of the new file
    print("Created file:", output_file)
```

