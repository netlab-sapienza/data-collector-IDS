from imports.fileManager import fileStorage
import re
import sys
import datetime
import string
import threading

from imports.ESPmanager import ESPutils
import subprocess
from multiprocessing import Process
from imports.utilities import firmwareManager
import os
import shutil

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # Python 3.x


ON_POSIX = 'posix' in sys.builtin_module_names

#threadLock = threading.Lock()

def main():

    if len(sys.argv) < 3:
        err_code = '0M'  # C stands for main
        err_mess = 'NOT ENOUGH INPUT ARGUMENTS'
        err_details = 'please pass the path of the firmware directory and the name of the output directory'
        raise ValueError(err_code, err_mess, err_details)

    if len(shutil.which("idf.py")) < 1:
        err_code = '1M'  # C stands for custom
        err_mess = 'NO ESP-IDF FRAMEWORK FOUND '
        err_details = 'ESPRESSIF ESP-IDF framework doesn\'t seem to be installed, impossible to find idf.py '
        raise ValueError(err_code, err_mess, err_details)




    fm =firmwareManager.FirmwareManager()

    file_stor = fileStorage.FileStorage()




    print("****** start ******")

    res_list_conn_esp = ESPutils.ESPutils.list_connected_esp()
    if res_list_conn_esp[0] > 0 or len(res_list_conn_esp[1]) < 1:
        err_code = '2M'  # C stands for custom
        err_mess = 'Error retrieving list of ESP32s '
        err_details = 'Impossible to retrieve the list of connected ESP32 boards or no ESP32 board found '
        raise ValueError(err_code, err_mess, err_details)

    processes_list =[]

    for esp_path in res_list_conn_esp[1]:
        esp_process =Process(target=__monitor_ESP__, args=(esp_path,) )       #ESPThread(esp_path)
        esp_process.start()
        processes_list.append(esp_process)
        #todo

    for p in processes_list:
        p.join()

    print("Exiting Main Thread of data-collector")


def __monitor_ESP__(esp_path):
    global threadLock  #shared tra i thread del singolo processo
    threadLock = threading.Lock()

    print("Process ",os.getpid(), "spawned by ",os.getppid(), "to manage ESP in ",esp_path)

    idf_path = shutil.which("idf.py")

    fm = firmwareManager.FirmwareManager()
    firmware_path = fm.getFirmwareDirPathStr()


    thread_list = []

    ret_val = subprocess.Popen( [idf_path,"-p",esp_path,"-C",firmware_path,"monitor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=ON_POSIX)

    #while ret_val.returncode is None:
     #   pass
    #else:
        #print("AAA : ", ret_val.returncode)
    #output ,errors = ret_val.communicate()
    #print("OUT ",output)
    #print("THREAD: output ",ret_val.stdout.readline())

    #ret_val = subprocess.run( [idf_path,"-p",esp_path,"monitor"],  capture_output=True, text=True)
    #output ,errors = ret_val.communicate()

    #if( ret_val.returncode ):
    #    print ("RUN failed\n\n%s\n\n" % (errors)   )

        #outQueue = Queue()
    #errQueue = Queue()

        #outThread = threading.Thread(target=enqueue_output, args=(ret_val.stdout, outQueue))
    #errThread = threading.Thread(target=enqueue_output, args=(ret_val.stderr, errQueue))

        #outThread.daemon = True
    #errThread.daemon = True

        #outThread.start()
    #errThread.start()



    while ret_val.returncode is None:

        try:
            #line = outQueue.get_nowait()  # or q.get(timeout=.1)
            line = ret_val.stdout.readline().decode("utf-8")   #bloccante


        except Empty:
            #print('no output yet')
            pass
        else:
            ts = datetime.datetime.now().timestamp()
            #print("PROCESS ", os.getpid(), " : ", line.rstrip())
            print("DEVICE ", esp_path, " : ", line.rstrip())
            #     sys.stdout.write(line) # print the monitor line on the stdout,in order to make the script transparent
            line_parser_t = LineThread(line, ts,esp_path)
            line_parser_t.start()
            thread_list.append(line_parser_t)
        ret_val.poll()

    errors = ret_val.stderr.read()
    print("ERRORS ",errors)

    for t in thread_list:
        t.join()



class LineThread(threading.Thread):
    def __init__(self, line, ts,esp_path):
        threading.Thread.__init__(self)
        self.line = line
        self.ts = ts
        self.esp_path = esp_path

    def run(self):
        __process_line__(str(self.line), self.ts,self.esp_path)


def __process_line__(line, ts,esp_path):
    global threadLock
    timestamp = int(ts * 1000000)
    # microseconds

    split_line = line.rstrip().split(" ")


    if len(split_line) > 4:
        if split_line[0][-1] == 'I' and split_line[2] == 'BenchMark:':
            # the line corresponds to a benchmark entry
            entry_to_store = str(timestamp)
            # todo: check on split_line[3] which must contain the ID of the ESP32
            for field in split_line[3:]:
                processed_field = ''.join(
                    list(filter(lambda x: x in string.printable, field)))  # remove non-printable characters

                processed_field = re.sub('[,]|(\[0m)$', '', processed_field)

                if len(processed_field) > 0:
                    entry_to_store = entry_to_store + ',' + processed_field
            print("ETS ", entry_to_store)
            entry_to_store = entry_to_store + '\n'



            f_s = fileStorage.FileStorage()
            esp_name = esp_path.split('/')[-1]

            threadLock.acquire()
            f_s.saveOnFile(esp_name,entry_to_store)
            threadLock.release()

    pass

# #### utils, valutare se spostare in utilities
#
# def enqueue_output(out, queue):
#     for line in iter(out.readline, b''):
#         queue.put(line)
#     out.close()
#
#
# def getOutput(outQueue):
#     outStr = ''
#     try:
#         while True: # Adds output from the Queue until it is empty
#             outStr+=outQueue.get_nowait()
#
#     except Empty:
#         return outStr





if __name__ == "__main__":
    main()