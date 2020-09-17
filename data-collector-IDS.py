from imports.fileManager import fileStorage
import re
import sys
import datetime
import string
import threading

from imports.ESPmanager import ESPutils




#threadLock = threading.Lock()

def main():
    print("first commit")
    olone = ESPutils.ESPutils.list_connected_esp()
    print(olone[1])

    # global file_stor
    # file_stor = fileStorage.FileStorage()
    #
    # #thread_list = []
    # for line in sys.stdin:
    #     ts = datetime.datetime.now().timestamp()
    #     sys.stdout.write(line) # print the monitor line on the stdout,in order to make the script transparent
    #     line_parser_t = myThread(line,ts)
    #     line_parser_t.start()
    #     #thread_list.append(line_parser_t)
    #
    # #for t in thread_list:
    # #    t.join()
    print("Exiting Main Thread of data-collector")


# class myThread (threading.Thread):
#     def __init__(self, line,ts):
#         threading.Thread.__init__(self)
#         self.line = line
#         self.ts = ts
#
#     def run(self):
#         __process_line__(str(self.line), self.ts)
#
# def __process_line__(line,ts):
#     global file_stor
#     timestamp = int(ts*1000000)
#     #microseconds
#
#     split_line = line.rstrip().split(" ")
#
#     if len(split_line) > 4:
#         if split_line[0][-1] == 'I' and split_line[2] == 'BenchMark:':
#             # the line corresponds to a benchmark entry
#             entry_to_store = str(timestamp)
#             #todo: check on split_line[3] which must contain the ID of the ESP32
#             for field in split_line[3:]:
#                 processed_field = ''.join(list(filter(lambda x: x in string.printable, field))) #remove non-printable characters
#                 processed_field = re.sub('[,]|(\[0m)$', '', processed_field)
#                 if len(processed_field) > 0:
#                     entry_to_store = entry_to_store + ',' + processed_field
#             entry_to_store = entry_to_store + '\n'
#
#             threadLock.acquire()
#             file_stor.saveOnFile(entry_to_store)
#             threadLock.release()
#
#     pass




if __name__ == "__main__":
    main()