import logging                                          # log error
import sys                                              # write log error file

# From Shai Ardazi on medium
class Logger:
    def __init__(self):
        # Initiating the logger object
        self.logger = logging.getLogger(__name__)
        
        # If logger has no handlers -> create one
        # Done to avoid logging MULTIPLE times (you MUST use this)
        if not self.logger.hasHandlers():
            # Set the level of the logger
            self.logger.setLevel(logging.WARNING)
            
            # Create the logs.log file
            handler = logging.FileHandler('logs.log')

            # Format the logs structure so that every line would include the time, name, level name and log message
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            
            # Adding the format handler
            self.logger.addHandler(handler)
            
            # And printing the logs to the console as well
            self.logger.addHandler(logging.StreamHandler(sys.stdout))