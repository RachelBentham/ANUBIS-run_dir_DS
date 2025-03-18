# this script gets all available Simulations from SS path and writes the full dataset to a csv table for putting arguments into condor submit scripts 

###To run: python read_scans_to_table.py -c config_hnl_madgraph.yaml
print("***Running script: read_scans_to_table.py***")

import os
#import glob
#import re
import pandas as pd # type: ignore
from processor_functions import *
import argparse
#import yaml # type: ignore

def GetParser():
    """Argument parser for reading scans script.."""
    parser = argparse.ArgumentParser(
        description="Processing simulations command line options."
    )
    parser.add_argument(
        "--userconfig",
        "-c",
        type=str,
        required=True,
        help="Specify the config for the user e.g. paths",
    )

    return parser

###Reading the specified config file for file paths
parser = GetParser()
args = parser.parse_args()
user_config_path = args.userconfig
user_config = load_config(user_config_path)
print("Using user config: ", user_config)
SS_path = user_config['SS_path']
llp_id = user_config['llp_id']

existing_df = pd.read_csv('samples_to_process.csv', index_col=0)    ###reads current contents of csv
if not existing_df.empty:
    max_index = existing_df.index.max()
else:
    max_index = -1 # starting from 0 if csv is empty 

print("***Finding SSs to add***")
# check existing_df for the SSX_prod_dec names, list their unique instances
print("Checking csv for existing SSs:")
existing_SSXs_array = existing_df['SS'].unique()
existing_SSXs_list = existing_SSXs_array.tolist()
print("Found: ", existing_SSXs_list)

# Find all SSXs in SS_path and save to list called SSXs
###Sort SSXs already in existing_df vs those to be added
print("Searching directory for new SSs:")
SSXs = []
SSXs_already_added = []
SSXs_to_add = []
#df_allscans = pd.DataFrame
for subdirpath, subdirnames, subfilenames in os.walk(SS_path):
    for subdirname in subdirnames:
        if subdirname.startswith("SS"):
            SSXs.append(subdirname)                         ###append all to SSXs
            if subdirname in existing_SSXs_list:            ###also append to _already_added or _to_add as appropriate
                SSXs_already_added.append(subdirname)
                print(f"SSX {subdirname} already in csv.")
            else:
                SSXs_to_add.append(subdirname)
                print(f"SSX {subdirname} not in csv - to be added.")
###Summarise: list all SSXs found and which sorted to each list
print("Summary of search:")
print("Simulation Swarms found in directory: ", SSXs)
print("of which SSs already matched with contents of csv are: ", SSXs_already_added)
print("and new SSs to add to csv are: ", SSXs_to_add)


# Get scans saved in available SSXs and convert to a lookup table to store data for SampleY's 
#for SSX in SSXs:

###If SSXs_to_add is empty, scan_to_df will return type NoneType, so update df only if it has non-zero length.
print("***Adding new SSs to dataframe***")
if len(SSXs_to_add) != 0:
    new_df = scan_to_df(SS_path, SSXs_to_add, llp_id) 
    print("New dataframe to add:")
    print(new_df)

    new_indices = range(max_index + 1, max_index + 1 + len(new_df))
    new_df.index = new_indices

    updated_df = pd.concat([existing_df, new_df])
    print("Updated dataframe:")
    print(updated_df)

    updated_df.to_csv("samples_to_process.csv", index=True)
    print("New SSs added to csv!")
else:
    print("No new SSs to add.")
