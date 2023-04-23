# Import Libraries
import os
import logging

# Debugging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "debug.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.DEBUG)

logging.info("Server Started")

def exec_command(cmd):
    # Run the job on Terminal
    logging.info("[COMMAND] " + cmd)
    os.system(cmd)
    return