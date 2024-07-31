import geopandas as gpd
import os
import subprocess
import shutil

# Provide the path to the folder of your gpkg file:
gpkg_path = "E://surfdrive//Tell_Kurdu_input_30072024//"

# Provide the name of the gpkg file (NOTE without .gpkg!) 
gpkg_name = "TK_T1112_P32224" 

# Create path to filename
gpkg_file = gpkg_path+gpkg_name+".gpkg"

template_gpkg = gpkg_path + "TK_TXXXX_PYYY.gpkg"


# Define the old and new names
old_layer_names = [
    "TK_TXXXX_PYYY_annotations",
    "TK_TXXXX_PYYY_elevation_differences",
    "TK_TXXXX_PYYY_elevations",
    "TK_TXXXX_PYYY_finds_samples",
    "TK_TXXXX_PYYY_graphic",
    "TK_TXXXX_PYYY_locus",
    "TK_TXXXX_PYYY_TEMP_locus",
    "TK_TXXXX_PYYY_unclear_locus_boundaries"
]

new_layer_names = [
    gpkg_name+"_annotations",
    gpkg_name+"_elevation_differences",
    gpkg_name+"_elevations",
    gpkg_name+"_finds_samples",
    gpkg_name+"_graphic",
    gpkg_name+"_locus",
    gpkg_name+"_TEMP_locus",
    gpkg_name+"_unclear_locus_boundaries"
]

# Function to copy and rename gpkg
def copy_and_rename_gpkg(template_gpkg, gpkg_file):
    shutil.copyfile(template_gpkg, gpkg_file)

# Function to rename layers in the GeoPackage
def rename_gpkg_layers(gpkg_file, old_layer_names, new_layer_names):
    for old_name, new_name in zip(old_layer_names, new_layer_names):
        # Use ogr2ogr to copy the layer with a new name
        subprocess.run([
            "ogr2ogr", "-f", "GPKG", gpkg_file, gpkg_file, "-nln", new_name, "-overwrite", old_name
        ])
        
        # Use ogrinfo to remove the old layer
        subprocess.run([
            "ogrinfo", gpkg_file, "-sql", f"DROP TABLE {old_name}"
        ])

# Rename the layers
rename_gpkg_layers(gpkg_file, old_layer_names, new_layer_names)

# Copy and rename the GeoPackage file
copy_and_rename_gpkg(template_gpkg, gpkg_file)


# Rename the layers
rename_gpkg_layers(gpkg_file, old_layer_names, new_layer_names)

print("Layer names updated successfully.")