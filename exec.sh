#!/bin/bash
source bin/activate

pip install adafruit-ampy
pip install esptool
esptool.py --port /dev/ttyUSB0 erase_flash
wget https://github.com/espressif/ESP8266_NONOS_SDK/archive/v2.2.1.zip
unzip v2.2.1.zip
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -e --flash_size=detect 0 esp8266-20220618-v1.19.1.bin
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0xffc000 ESP8266_NONOS_SDK-2.2.1/bin/esp_init_data_default_v08.bin
#esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-1m-20220618-v1.19.1.bin
#esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-512k-20220618-v1.19.1.bin
