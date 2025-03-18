import pandas as pd # type: ignore
import os
import argparse
from processor_functions import *

job_dir = "/usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/job_submit/"
madgraph_config = "/usera/rcb72/Documents/Higgs_Dark_Scalar/run_dir_DS/config_madgraph_DS.yaml"
mg_config = load_config(madgraph_config)
selection_config = "/usera/rcb72/neo-set-anubis/db/DarkScalar/PaulSelection/configs/config_selection_DS.yaml"
sel_config = load_config(selection_config)

scanfile = mg_config['scanfile']          ###Used to get indices of runs to process
df = pd.read_csv(scanfile, index_col=0)
indices = df.index

# template condor job submission file
job_template = """
executable = select_DS.sh
arguments = {index} {config_argument}
output = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/out/job_selection_{index}.out
error = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/err/job_selection_{index}.err
log = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/log/job_selection_{index}.log
getenv = true
Requirements = (HAS_r04)
#Requirements = (HAS_r04 && OpSysAndVer == "AlmaLinux9") # Do I want to run on a node running alma9? Will cvmfs depend on this setting? 
#machine_count = 2
request_cpus = 5
request_memory = 2G
request_disk = 1024M
when_to_transfer_output = ON_EXIT
max_retries = 2    
queue
"""

for index in indices:
    job_file_content = job_template.format(index=index, config_argument=selection_config)
    job_file_name = job_dir+f'job_selection_{index}.submit'

    # write job submit file
    with open(job_file_name, 'w') as job_file:
        job_file.write(job_file_content)

    # submit to condor
    os.system(f'condor_submit {job_file_name}')
    print("Submitted job") 

