MFRC522-python
==============
A small class to interface with the NFC reader Module MFRC522 on the Raspberry Pi.

This is a Python port of the example code for the NFC module RF522-AN.

## Table of Contents
1. [Install on Raspberry Pi running Jessie](#install-on-raspberry-pi-running-jessie-)
2. [Install on Raspberry Pi running Wheezy](#install-on-raspberry-pi-running-wheezy-)
3. [Usage](#usage)
4. [Useful Resources](#useful-resources)
5. [Disclaimer](#disclaimer)

## Install on Raspberry Pi running **Jessie**
### 0 – Latest Kernel
Make sure you have the latest kernel (>= ```4.4.14```), because it fixes a bug in earlier version [Issue #1547](https://github.com/raspberrypi/linux/issues/1547#issuecomment-230170202).
You can check your version using:
```
uname -a | sed -E "s/.*([0-9]+\.[0-9]+\.[0-9]+)-v.*/\1/"
```

If you need to update your kernel, use ```sudo rpi-update```. If it's not yet installed, do so using ```sudo apt-get install rpi-update```.

### 1 – Wiring
| RF522 Module | Raspberry Pi          |
| :----------- | :-------------------- |
| SDA          | Pin 24 / GPIO8 (CE0)  |
| SCK          | Pin 23 / GPIO11 (SCKL)|
| MOSI         | Pin 19 / GPIO10 (MOSI)|
| MISO         | Pin 21 / GPIO9 (MISO) |
| IRQ          | –                     |
| GND          | GND                   |
| RST          | Pin 22 / GPIO25       |
| 3.3V         | 3.3V                  |

### 2 – Activate SPI
```
sudo raspi-config
```
And then go to ```9 – Advanced Options``` > ```A5 SPI``` and enable the SPI interface.
Reboot (```sudo shutdown -r now```).
You can verify a successful configuration by entering
```
ls /dev/spi*
```
The output should be similar to the following, thus confirming the existence of the necessary sockets.
```
/dev/spidev0.0  /dev/spidev0.1
```

### 3 – Install Software
Make sure you have Python and Git installed:
```
sudo apt-get install git python3-dev --yes
```
#### 3.1 – SPI-Py
```
git clone https://github.com/mab5vot9us9a/SPI-Py && cd SPI-Py
sudo python3 setup.py install
cd ..
```

#### 3.2 – Raspberry Pi RFID RC522 Library
```
git clone https://github.com/mab5vot9us9a/MFRC522-python.git && cd MFRC522-python
```

### 4 – Check everything's working
```
python3 Dump.py
```
and place your tag (MIFARE Classic 1K (S50)) on the reader to dump its data.

## Install on Raspberry Pi running  **Wheezy**
Follow these instructions: [RASPBERRY PI RFID RC522 TAGS AUSLESEN (NFC)](http://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/).


## Usage
Import the class by importing MFRC522 in the top of your script. For more info see the examples.

## Useful Resources
- [MiFare Byte Layout](https://en.wikipedia.org/wiki/File:MiFare_Byte_Layout.png#file)
- [MIFARE Classic EV1 1K Data Sheet](http://cache.nxp.com/documents/data_sheet/MF1S50YYX_V1.pdf)

# Disclaimer
Instructions adapted from [tutorials-raspberrypi.de](http://tutorials-raspberrypi.de/).  
Original source code: https://github.com/mxgxw/MFRC522-python.
