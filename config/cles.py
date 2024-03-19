# Change these to match the site
REMOTE_HOST = '209.165.155.4'           # Hostname or IP address of remote host
REMOTE_PORT = 5822						# Port number to connect on
REMOTE_USER = 'novac'                              # Username for logging into remote host
REMOTE_PASSWORD = '1225'                       # Password for the above user
REMOTE_DIRECTORY = '/mnt/flash/novac' # Directory on the remote host containing files we want to transfer
REMOTE_FILE_PATTERN = "*.pak"                       # Pattern for matching desired files
EXCLUDE_FILE_WORD = "upload"                       # Pattern for excluding files
#LOCAL_SAVE_DIRECTORY = 'C:\\Users\\novac\\Desktop\\NOVAC-Incoming\\MAYP115415' # Where on the machine running this script to save the transfered files.
LOCAL_SAVE_DIRECTORY = 'W:\\NOVAC\\NOVAC-Incoming\\r0a0'