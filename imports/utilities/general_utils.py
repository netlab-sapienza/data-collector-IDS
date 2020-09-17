#this class contains static methods which perform some generic utilities
from pathlib import Path
import os



class General_utils:
    @staticmethod
    def list_directory_content_array(dir:Path) -> [str]:
        return 0,[f for f in os.listdir(dir)]

