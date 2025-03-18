import pandas as pd # type: ignore
import os
import argparse
from processor_functions import *
index = 0
job_dir = "/usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/job_submit/"
madgraph_config = "/usera/rcb72/Documents/Higgs_Dark_Scalar/run_dir_DS/config_madgraph_DS.yaml"
mg_config = load_config(madgraph_config)

jobscripts_path = mg_config['jobscripts_path']
#jobscripts_path = "/usera/rcb72/Documents/Higgs_Dark_Scalar/MG_Inputs"

# template condor job submission file
job_template = """
executable = MG_simulations.sh
arguments = {index} {jobscript_path}
output = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/out/job_MG_{index}.out
error = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/err/job_MG_{index}.err
log = /usera/rcb72/Documents/Higgs_Dark_Scalar/CondorFiles/log/job_MG_{index}.log
getenv = true
Requirements = (HAS_r04)
#Requirements = (HAS_r04 && OpSysAndVer == "AlmaLinux9")
#machine_count = 2
request_cpus = 5
request_memory = 512M
request_disk = 1024M
when_to_transfer_output = ON_EXIT
max_retries = 2    
queue
"""

jobscript_names = [f for f in os.listdir(jobscripts_path) if os.path.isfile(os.path.join(jobscripts_path, f))]
for jobscript_name in jobscript_names:
    print(f"jobscript name: {jobscript_name}")

    jobscript_filepath = os.path.join(jobscripts_path, jobscript_name)
    job_file_content = job_template.format(index=index, jobscript_path=jobscript_filepath)
    job_file_name = job_dir+f'job_MG_{index}.submit'

    # write job submit file
    with open(job_file_name, 'w') as job_file:
        job_file.write(job_file_content)

    # submit to condor
    os.system(f'condor_submit {job_file_name}')
    print("Submitted job") 
