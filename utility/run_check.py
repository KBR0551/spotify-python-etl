import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.getcwd())+"/.env")

def run_check(exec_script_nm,curr_dt):
    if os.path.exists(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json"):
        x=open(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json")
        data=json.load(x)
        if exec_script_nm in data and data[exec_script_nm]==curr_dt:
            return 'Y',curr_dt
        else:
             x.close()
             data[exec_script_nm]=curr_dt
             return 'N',data
    else:
        return 'N',{exec_script_nm : curr_dt}




