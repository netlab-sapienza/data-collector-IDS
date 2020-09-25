# data-collector-IDS
This repo contains the new data-collector script used to collect data for BLE-mesh IDS from ESP boards

## Introduction 
This script performs the following actions:
- identifies all the ESP32 boards connected via USB
- launches the **monitor** function corresponding to firmware in the directory passed as argument
- creates a .csv file for each connected device in the directory ../results/name_passed_as_arg_timestamp
- collects all the log entries with the tag "BenchMark", splits the words in the body of the log and saves an entry into the csv file corresponding to the source ESP32

## Requirements

- The chosen firmware must be already flashed into the ESP32 boards
- ESPRESSIF's ESP-IDF framework must be installed, follow the guide (https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html)
- Python3

## Usage


```bash
cd data-collector-IDS
python3 data-collector-IDS.py firmware-path output-directory-name
```
**firmware-path** [Mandatory] must be the path containing the script to launch, 
  the script looks for "sdkconfig" file inside the passed directory to recognize it as a valid firmware. </br>
**output-directory-name** [Mandatory] must be the name of the desired output directory, it can only contain **letters numbers - _ **, no space allowed </br>

To terminate the script press ctrl+] until the execution stops (an error is launched), then ctrl+c

Output .csv files will be found in the directory containing the script, in ../results/output-directory-name_timestamp
