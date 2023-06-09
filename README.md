# AIS_Barcin_QGIS
This repository contains a series of scripts that allows to process that data for the archaeoligical information system for the excavation activities for the site Barcin Hoyuk.

## Setup 
(Note that these setup instructions have been copied from --> https://carpentries-incubator.github.io/deep-learning-intro/setup/)

1. Open https://www.anaconda.com/products/distribution with your web browser.
2. Download the Python 3 installer for Windows.
3. Double-click the executable and install Python 3 using MOST of the default settings. The only exception is to check the Make Anaconda the default Python option.

Once you installed anaconda, please open the terminal of Anaconda by pressing the windows button and type "Anaconda prompt".

### Creating the environment
To make sure your python installation is not conflicting with anthing else we are going to creat a environment called ais_barcin and install the required libraries. Open a terminal and type the command:

```
conda create --name ais_barcin python jupyter pandas
```

Now we are going to activate the newly created environment:
```
conda activate ais_barcin
```

Next we are going to install the necessary libraries for the script that has been developed using pip. We will probably get a lot of notifications that some have already been installed. 

Installing Geopandas
```
pip install geopandas
```

Install shapely

```
pip install shapely
```
The libraries shutil, os and glob are installed with the default version of python´s anaconda.

Once these libraries have been installed open a jupyter notebook by typing the following in your terminal. (when you lateron want to open jupyter lab you need to open you termimal directly, make sure to activate ais_barcin and type jupyter notebook. 

```
jupyter notebook
```

# Data processing AIS Barcin -> Vector data

## Step 0:  Import libraries

Open a new notebook (right top New - python 3) and copy the following code in the first line. 

```python
import shutil 
import pandas as pd
import glob
import os
import geopandas as gpd
from shapely.geometry import Point
```

If there are no errors when running this script we are all set to run our script. 
Keep the first cell and continue with the code below.

## Step 1:  Defining folder locations

Add the following code in the next cell and run it. This will define the variables for the locations of the GIS files 
```python
#Define the variables for the locations of the GIS files
org_GIS = input("Fill in path to GIS folder, eg C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\ : ")
loc_output = input("Fill in path where to create the OUTPUT folder:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\ : ")
#Create the output folder
os.system('md ' + loc_output + 'OUTPUT')
```
Once you run this cell you will be asked to fill in the location of the GIS folder containing the files.

Next, download [Barcin_Hoyuk_GIS_QGIS.qgz](https://github.com/SPINLab/AIS_Barcin_QGIS/blob/main/Barcin_Hoyuk_GIS_QGIS.qgz) and store in the folder where you want the OUTPUT folder to be created. This file will be usefull to browse through your data in [QGIS](https://www.qgis.org/en/site/).

## Step 2:  Add filename to all shapefiles
```python
#Step 2 add the filename of the original shapefile as a collumn so it is always clear where an object came from.
#Create a list of all the shapefiles in the folder
file_pattern = '**/*.shp'
file_list = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)
#Remove the TEMP layer from the list
file_list = [f for f in file_list if '_TEMP' not in os.path.basename(f)]
#Remove all the template files from the list
file_list = [item for item in file_list if "RENAME" not in item]
#Read the list and add the shapefile name
for file in file_list:
    # Open the shapefile with Geopandas
    gdf = gpd.read_file(file)
    # Get the filename of the shapefile without the extension
    filename = os.path.splitext(os.path.basename(file))[0]

    # Add a new column to the attribute table and populate it with the filename
    gdf['shpname'] = (filename)
    index_cols = [col for col in gdf.columns if 'index' in col]
    if index_cols:
        gdf = gdf.drop(index_cols, axis=1)
    level_0_cols = [col for col in gdf.columns if 'level_0' in col]
    if level_0_cols:
        gdf = gdf.drop(level_0_cols, axis=1)
    # Save the modified shapefile
    gdf.to_file(file)
```

## Step 3: create a merged shapefile for locus layer

Copy the following in the next cell and run.

```python
#Step 3 create the Locus layer
#Put all the locus files from the various folders in a list 
file_pattern = '**/*_locus.shp'
file_list = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)

#Remove the TEMP locus layer from the list
file_list = [f for f in file_list if '_TEMP' not in os.path.basename(f)]
#Remove all the template files from the list
file_list = [item for item in file_list if "RENAME" not in item]

#Merge all the locus files from the list
#Read in each shapefile as a GeoDataFrame
gdfs = [gpd.read_file(shapefile) for shapefile in file_list]

#Concatenate the GeoDataFrames into one
merged_gdf = pd.concat(gdfs, ignore_index=True)

#Convert back to a GeoDataFrame
merged_gdf = gpd.GeoDataFrame(merged_gdf, crs=gdfs[0].crs, geometry='geometry')

#Save the merged shapefile
merged_gdf.to_file(loc_output+'OUTPUT\\BH_locus.shp')
shp_output = loc_output+'OUTPUT\\BH_locus.shp'
```

## Step 4: create joinfld

Copy the following in the next cell and run it.

```python
#Step 4 Create the joinfld in the newly created locus file
#Read in the shapefile as a geopandas GeoDataFrame
gdf = gpd.read_file(shp_output)

col1 = 'Trench'
col2 = 'Locus'

# Add the new field to the GeoDataFrame
gdf['joinfld'] = gdf.apply(lambda row: row[col1] + '_' + str(int(row[col2])), axis=1)

#Drop collumns
gdf = gdf.drop(['index'], axis=1)

# Write the updated GeoDataFrame to a new shapefile
gdf.to_file(shp_output)
```


## Step 5: Create centroid point with labels of locus
Copy the code below and run it. 
```python
#Step 5 Create centroid point with labels of locus
# Define the paths to locus polygon shp polygon and the point shapefile to be created
poly_path = loc_output+'OUTPUT\\BH_locus.shp'
point_path = loc_output+'OUTPUT\\BH_locus_points.shp'

# Open the polygon shapefile with Geopandas
poly_gdf = gpd.read_file(poly_path)

# Calculate the centroid of each polygon
centroids = poly_gdf['geometry'].centroid

# Create a new Geopandas GeoDataFrame with the centroids as points
point_gdf = gpd.GeoDataFrame(poly_gdf.drop('geometry', axis=1), crs=poly_gdf.crs, geometry=centroids)

# Save the new point shapefile
point_gdf.to_file(point_path)
```

## Step 6: Create merged layers for all other files

```python
#Step 6 Create merged layers for all other files
type_list = ['annotation','heights','height_differences','graphic','finds_samples','unclear_limits','underlying_level_lines','underlying_level_polygons']

for item in type_list:
    file_pattern = '**/*_'+item+'.shp'
    file_list2 = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)
    file_list2 = [item for item in file_list2 if "RENAME" not in item]
    # read in each shapefile as a GeoDataFrame    
    gdfs = [gpd.read_file(shapefile).to_crs('EPSG:2320') for shapefile in file_list2]
    merged_gdf = pd.concat(gdfs, ignore_index=True)
    merged_gdf = gpd.GeoDataFrame(merged_gdf, crs=gdfs[0].crs, geometry='geometry')
    merged_gdf.to_file(loc_output+'OUTPUT\\BH_'+item+'.shp')
    file_list2 =[]
    print(item)
```

Now go to the access database and export the locus table to the database folder and name it: DATABASE\3_Locus.csv make sure to add the field names on the first row and select the ; as deliminator. 

If everything went well please open the Barcin_Hoyuk_GIS_QGIS.qgz file you stored above. 

# Create QLR files

In order to load seperate layers qlr files for every plan, the script below can be used. Based on the locus layer shpname seperate qlr files can be created. Before you do this make sure to have the [AAAA.qlr](https://github.com/SPINLab/AIS_Barcin_QGIS/blob/main/AAAA.qlr) or download a zip file [AAAA.zip](https://github.com/SPINLab/AIS_Barcin_QGIS/blob/main/AAAA.zip) unzip it and store it in the folder QLR in your project folder. (e.g. C:\... Barcin\QLR\AAAA.qlr)

``` python
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


# Data processing AIS Barcin -> Raster data

The script below is a fairly simple script that allows you to copy all files with a certain extension to a new folder without integrating the sub folders. 

This script can be downloaded [here](https://github.com/SPINLab/AIS_barcin_hoyuk/blob/master/FOSS_python3/copy_files_with_extentions_py3.py) or run in the jupyter notebook by copy pasting the code below. 

```python
#This script allows you to copy all files with a certain extension to a new folder without integrating the sub folders
#Created by Maurice de Kleijn Vrije Universiteit Amsterdam Spatial Information laboratory for the datamanagement 
#of the the archaeological project Barin Hoyuk 22062016 Python 2.7 updated 14/04/2023 for python 3.x

import shutil
import os

org_GIS = input("provide path to GIS folder in dropbox : eg. C:\Dropbox\Barcin_Hoyuk\AIS_Barcin_Hoyuk\AIS\GIS\: ")
outputfolder = input("provide path to output folder : eg. C:\Temp\: ")
ext = input("provide extension type to be copied eg .tif or .jpg :")

os.system('dir ' + org_GIS + '*' + ext + ' /s/d/b >' + org_GIS + 'tempext.txt')

file1 = open(org_GIS + 'tempext.txt', 'r')
lines = file1.readlines()

for line in lines:
    ln = line.rstrip('\n')
    shutil.copy(ln, outputfolder)
    file1.close()

os.system('del ' + org_GIS + 'tempext.txt')
```


