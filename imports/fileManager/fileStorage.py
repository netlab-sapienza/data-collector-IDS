#TODO

from imports.utilities.singleton import Singleton
from imports.ESPmanager.ESPutils import ESPutils
from pathlib import Path
import os
import re
from random import randrange
import datetime
import time

import sys


class FileStorage(metaclass=Singleton):

    def __init__(self):
        self.__ready = False

        self.__output_directory_path = ''
        self.__file_desc_dict = {}

        self.__checkValidityOutputDIRName()

        self.__initializeOutputDir()

        self.__initializeFileDescrDictionary()

        self.__ready = True



    def saveOnFile(self,dev_name,content):
        while not self.__ready:
            #thread is blocked,sleep forces yel
            time.sleep(0.000001)


        if str(dev_name) not in self.__file_desc_dict:
            err_code = '1C'  # C stands for custom
            err_mess = 'TRYING TO SAVE ON A NON-EXISTING FILE '
            err_details = 'Called saveOnFile passing a wrong argument for dev_name, the file does not exist'
            raise ValueError(err_code, err_mess, err_details)

        self.__file_desc_dict[str(dev_name)].write(content)
        self.__file_desc_dict[str(dev_name)].flush()



    def __checkValidityOutputDIRName(self):

        if len(sys.argv) < 3:
            err_code = '1C'  # C stands for custom
            err_mess = 'NO DIRECTORY PASSED AS ARGUMENT'
            err_details = 'please pass the name of a directory where to store results as argument'
            raise ValueError(err_code, err_mess, err_details)


        output_dir_name_check = bool(re.match('^[a-zA-Z0-9\-_]+$', str(sys.argv[2])))

        if not output_dir_name_check:
            err_code = '2C'  # C stands for custom
            err_mess = 'INVALID NAME FOR THE OUTPUT DIRECTORY'
            err_details = 'please pass a name containing only letters/numbers/-/_  and no whitespace '
            raise ValueError(err_code, err_mess, err_details)

    def __initializeOutputDir(self):

        script_root_path = Path(Path(str(sys.argv[0])).resolve().parent.parent)

        output_dir_path = script_root_path.joinpath('results').joinpath(
            str(sys.argv[2]) + '_' + str(datetime.datetime.now().timestamp()))
        print("Checking if ./results/  exists...")
        try:
            os.makedirs(script_root_path.joinpath('results'))
        except OSError as e:
            print("./results/ already exists, continuing... ")

        try:
            os.makedirs(output_dir_path)
        except OSError as e:
            err_code = '3C'  # C stands for custom
            err_mess = 'ERROR CREATING THE OUTPUT DIRECTORY'
            err_details = 'Impossible to create the output directory, DUMP: ', e
            raise ValueError(err_code, err_mess, err_details)

        print("Output Dir initialized")
        self.__output_directory_path = str(output_dir_path)


    def __initializeFileDescrDictionary(self):

        res_list_conn_esp = ESPutils.list_connected_esp()
        if res_list_conn_esp[0] > 0 or len(res_list_conn_esp[1]) < 1:
            err_code = '0C_main'  # C stands for custom
            err_mess = 'Error retrieving list of ESP32s '
            err_details = 'Impossible to retrieve the list of connected ESP32 boards or no ESP32 board found '
            raise ValueError(err_code, err_mess, err_details)

        pass

        res_list_conn_esp_split = [x.split('/')[-1] for x in res_list_conn_esp[1]  ]

        for elem in res_list_conn_esp_split:

            if len(elem)< 1:
                err_code = '1C_main'  # C stands for custom
                err_mess = 'Error creating the name for output file '
                err_details = 'Impossible to create the output filename, something went wrong... abort '
                raise ValueError(err_code, err_mess, err_details)

            self.__initializeNewFile(elem)


#todo: BISOGNA CREARE UN FILE PER OGNI esp32 COLLEGATO, NON UN SINGOLO FILE
    def __initializeNewFile(self,device_name):
        filename = self.__output_directory_path + "/" + str(device_name) + ".csv"
        self.__file_desc_dict[str(device_name)] = open(filename, 'a+')


