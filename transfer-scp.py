import fnmatch
import glob
import importlib
import logging
import os
import sys

from pathlib import Path

from paramiko import SSHClient, WarningPolicy
from scp import SCPClient

# Make sure we start in the same directory as this file lives in, regardless of how we were called.
os.chdir(os.path.dirname(__file__))

####### RUNTIME CONFIGURATION ################
# Directory containing config files
CONFIG_PATH = os.path.abspath('../config')

# Logging setup. Create handlers to log to stdout, files, etc as desired
# Add a stream handler to output to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# Add desired logging handlers to this list
log_handlers = [stream_handler]
########## END RUNTIME CONFIGURATION ########
def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

def transfer_files(conf_file):
    logging.info("Beginning transfer for %s", conf_file)
    CONFIG = importlib.import_module(conf_file)
    
    # Make sure the local save directory exists
    os.makedirs(CONFIG.LOCAL_SAVE_DIRECTORY, exist_ok=True)
    
    # And change into it
    os.chdir(CONFIG.LOCAL_SAVE_DIRECTORY)
    
    # Connect to the remote host
    with SSHClient() as ssh:
        # Don't check the hostkey
        ssh.set_missing_host_key_policy(WarningPolicy())

        ssh.connect(CONFIG.REMOTE_HOST, port = CONFIG.REMOTE_PORT, username = CONFIG.REMOTE_USER, password = CONFIG.REMOTE_PASSWORD)
        logging.info("Connected to remote server")    
        
        stdin, stdout, stderr = ssh.exec_command(f"cd {CONFIG.REMOTE_DIRECTORY} && ls")
        files = [line.strip() for line in stdout]
        logging.debug(f"Directory list is: {files}")
        # files = fnmatch.filter(files, CONFIG.REMOTE_FILE_PATTERN)
        files = [file for file in fnmatch.filter(files, CONFIG.REMOTE_FILE_PATTERN) if CONFIG.EXCLUDE_FILE_WORD not in file]
        logging.info(f"Got file list of: {files}")
        with SCPClient(ssh.get_transport(), progress=progress, socket_timeout=180) as scp:
            # We are in the directory we want to save the files to, so no need to specify 
            # local directory
            
            for file in files:
                file_path = CONFIG.REMOTE_DIRECTORY+"/"+file
                logging.info("Transfering file %s", file)
                
                # Download the file
                scp.get(file_path, local_path="temp.transfer")
                
                # Rename the file to the final name after downloading is complete
                os.rename('temp.transfer', file)
                
                # And remove it from the remote server
                logging.info("Removing %s from remote server", file)
                ssh.exec_command(f"rm '{file_path}'")    


if __name__ == "__main__":    
    logging.basicConfig(
        level = logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = log_handlers
    )
    logging.debug("Adding %s to the search path", CONFIG_PATH)
    sys.path.append(CONFIG_PATH)
        
    logging.info("Beginning processing")

    all_configs = glob.glob(os.path.join(CONFIG_PATH, "*.py"))
    logging.debug("Processing config files in: %s", str(all_configs))
    for conf_file in all_configs:
        conf_file = str(Path(conf_file).with_suffix('').name)
        transfer_files(conf_file)
        
    logging.info("Transfer process complete")

 