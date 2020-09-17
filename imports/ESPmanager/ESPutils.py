from pathlib import Path
import re

from imports.utilities.general_utils import General_utils


class ESPutils:
    @staticmethod
    def list_connected_esp() -> [str]:
        my_path = Path('/dev').absolute()

        content_array_res = General_utils.list_directory_content_array(my_path)
        if content_array_res[0] > 0:
            print("ERRR")
            #todo


        status = 0 #this is the error flag, set it to 1 if process cannot complete
        if len(content_array_res[1]) < 1:
            status = 0
            boards = []
        else:

            boards = [f for f in content_array_res[1] if bool(re.match('^(ttyUSB)[0-9]+$', f)) ]
            #boards = [f for f in content_array_res[1]]

            print("AAAAAA   ",content_array_res[1])
            print("BBBBBB    ", boards)


        return status,boards