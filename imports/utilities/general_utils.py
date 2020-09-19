#this class contains static methods which perform some generic utilities
from pathlib import Path
import os



class General_utils:

    #lists all files and directories in the given directory dir (Path)
    #IMP: it throws an error if the passed directory does not exist
    @staticmethod
    def list_directory_content_array(dir:Path) -> [str]:
        return 0,[f for f in os.listdir(dir)]

