from .singleton import Singleton
from pathlib import Path
import datetime
import sys
import re
import os



class FirmwareManager(metaclass=Singleton):
    def __init__(self):
        self.__firmware_dir_path = self.__firmware_dir_path_validator()[1]


    def __firmware_dir_path_validator(self):


        if len(sys.argv) < 2:
            err_code = '2C'  # C stands for custom
            err_mess = 'MISSING FIRMWARE DIRECTORY NAME'
            err_details = 'please pass the name of the directory containing the ESP32 firmware'
            raise ValueError(err_code, err_mess, err_details)

        #input_dir_name_check = bool(re.match('^[a-zA-Z0-9\-_]+$', str(sys.argv[1])))

        # if not input_dir_name_check:
        #     err_code = '3C'  # C stands for custom
        #     err_mess = 'INVALID NAME FOR AN INPUT DIR'
        #     err_details = 'please pass a name containing only letters/numbers/-/_  and no whitespace '
        #     raise ValueError(err_code, err_mess, err_details)

        firmware_dir_path = Path(str(sys.argv[1])).resolve()

        if not firmware_dir_path.is_dir():
            err_code = '3C'  # C stands for custom
            err_mess = 'NO FIRMWARE DIRECTORY FOUND '
            err_details = 'no firmware found at ' + str(firmware_dir_path)
            raise ValueError(err_code, err_mess, err_details)


        if not firmware_dir_path.joinpath('sdkconfig').is_file():
            err_code = '3Cbis'  # C stands for custom
            err_mess = 'NO FIRMWARE DIRECTORY FOUND '
            err_details = 'no firmware found at ' + str(firmware_dir_path) +" , no sdkconfig file found in the given directory"
            raise ValueError(err_code, err_mess, err_details)

        return 0, str(firmware_dir_path)




    def getFirmwareDirPathStr(self):
        return self.__firmware_dir_path

