# AIS_Barcin_QGIS
This repository contains a series of scripts that allows to process that data for the archaeoligical information system for the excavation activities for the site Barcin Hoyuk.

## Setup 
(Note that these setup instructions have been copied from --> https://carpentries-incubator.github.io/deep-learning-intro/setup/)

1. Open https://www.anaconda.com/products/distribution with your web browser.
2. Download the Python 3 installer for Windows.
3. Double-click the executable and install Python 3 using MOST of the default settings. The only exception is to check the Make Anaconda the default Python option.

Once you installe anaconda, please open the terminal of Anaconda. This can be done by the windows command and type "cmd" you will see a

To create a conda environment called dl_workshop with the required packages, open a terminal by pressing the windows button and type "Anaconda prompt".

### Creating the environment

To create a conda environment called ais_barcin with the required packages, open a terminal and type the command:

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
Install shutil 

```
pip install shutil 
```
Install glob

```
pip install glob
```
Install os

```
pip install os
```
Install shapely

```
pip install shapely
```

Once these libraries have been installed open a jupyter notebook by typing the following in your terminal. (when you lateron want to open jupyter lab you need to open you termimal directly, make sure to activate ais_barcin and type jupyter notebook. 

```
jupyter notebook
```

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

## Step 1:  Setting the references to the folders 

Add the following code in the next cell and run it. This will define the variables for the locations of the GIS files 
```python
#Define the variables for the locations of the GIS files
org_GIS = input("Fill in path to GIS folder, eg C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\: ")
loc_output = input("Fill in path where to create OUTPUT folder:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")
#Create the output folder
os.system('md ' + loc_output + 'OUTPUT')
´´´

Now make sure to download this file 

## Step 2:  Setting the references to the folders
Next wel are 





