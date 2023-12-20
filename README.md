# RaspberryPi LoRa Communication README
---
## Introduction
Project was under development during the second semester of Master studies in Embedded Systems field on **Warsaw Univeristy of Technology**. Project was a part of a total of three mini-projects as part of the **Internet of Things** (pol. *Internet Rzeczy*) classes.

The main goal of the project was to establish a connection between **two Raspberry Pi 3 SBCs** (ang. Single Board Computers) using a LoRa protocol. Every Raspbbery Pi had its own Dragino LoRa/GPS hat which enables setting up a communiaction. As mentioned, the hat is equipped with a GPS module, although it wasn't tested and used in this project. For data sent we chose an avarge RGB value of the picture taken by PiCamera. It is stored as a text-file. The file is then opened and the data is transmited via LoRa protocol to the receiver which writes an incoming messege into its own text-file.

## Before moving on into README
The recommended OS for this project is **Raspbian OS 32-bit** as the WiringPi library works best on this software. Make sure you've installed the right OS as our program may not work on the 64-bit version.

## Important links & files

Below are the two most important links which content was heavily "explored" during development of this project. The first one is referencing the main page of the WiringPi library home page. The second one is referencing specifically the *News* section of the library, where you can find more examples than shown below in the **Quick Setup** section.

[WiringPi library docs](http://wiringpi.com/)\
[WiringPi news](http://wiringpi.com/news/)

Look also into the PDF file in PDF-DocFiles directory for a specific step-by-step installation. In the project, **chapter 4** titled <u>Example3: Two RPI use LoRa to transmit to each other</u>, was used.

## Quick setup
Quick setup is recommended to test the functionality of the LoRa librarry. Although all of the code below can be find in the links given above and in the mentioned PDF file, we decide to also write it here, because we value your time. :)

1. First of all, remember to make sure that the SPI, Serial Port and Serial Console interfaces are enabled in the Raspberry Pi Configuration. You can enter it using top-left corner menu or by typing **sudo raspi-config** in the terminal.

2. Installation of WiringPi.h library for Raspberry Pi 3 - written in C.
```
cd /tmp

wget https://unicorn.drogon.net/wiringpi-2.46-1.deb

sudo dpkg -i wiringpi-2.46-1.deb
```

3. Downloading the lora transceiver source files:
```
wget https://codeload.github.com/dragino/rpi-lora-tranceiver/zip/master

unzip master
```

4. Run a make file.
```
cd rpi-lora-tranceiver-master/dragino_lora_app

make
```

5. Run the app (sender or rec (receiver))
```
./dragino_lora_app sender
./dragino_lora_app rec
```

Remember that every change in the main.c source file requiers performing steps 4. and 5. once again.


## Project files description
Project is mainly divided into two parts: one responsible for handling the LoRa communication and the second one handling the PiCamera and image analysis. 

Directory "PDF-DocFiles" contains all the files (.pdf format) which where considered worth putting in for the future developers. At the moment there is only one file, which is the LoRa hat datasheet.

Directory "cameraAnalysis" contains two files:
- camera.py -- there is only one function responsible for taking a shot using PiCamera and storing it in the main directory.
- ImageAnalyzer.py -- class written to make code clearer and easy-expandable. The main goal of this class is to calculate average RGB of an image but many other functionalities can by easily implemented.

Directory "lora-comm" contains all the files used in the process of communication between two Raspberry Pis. As mentioned above all the necessary functions are located in the **main.c** file. Feel free to add your own functionality, but be careful. It's a "fragile being". :)

---
---

**IMPORTANT:**\
Files for LoRa communication used in this project are located in the "dragino_lora_app" directory. The other two directories are included into the package delivered by the manufacturer of the LoRa module.

---
---

The most important file is the *main.c* file including all the code needed for the LoRa protocol. File *Makefile* contains rules for the **make program**. Two more files:
- main.o -- object file being the effect of comipilation
- dragin_lora_app -- executable file ready to be run

Located in the main directory file **app.py** is responsible for taking a shot using PiCamera, calculate its average RGB and finally writing results into text file. Its also responsible for generating "RPi-camphoto.jpg" file in the main directory.

## Starting the application

### Introducion
Runing the application can be done simply by runing **setup_tx.sh** and **setup_rx.sh** files. But please take it into account that those scripts already run the application for you. So **DO NOT** run both scripts at once.

Run the **setup_tx.sh** on your tranceiver device (the one with camera).

Run the **setup_rx.sh** on your receiver device.

Tip: it is better to run these scripts through the terminal using the ```sudo bash setup_name_file.sh``` command.

### First run
If it's the first time your Raspberry runs our program, please make sure that you uncomment code written between the '='-lines in both files: **setup_tx.sh** and **setup_rx.sh**.

### Second and every next run
If it's not the first time your Raspberry runs our program, just run **setup_tx.sh** and **setup_rx.sh** respectively on the tranceiver and receiver device. If you edited these files before, make sure you commented sections mentioned above.

## Getting GPS to work

### Enable the UART
To begin, it's essential to acquire and set up a new device tree overlay. Raspberry Pi Engineer PhillE, known as "PhillE" on the forums, has thoughtfully crafted a specialized overlay named pi3-miniuart-bt-overlay.dtb. This file  This overlay is designed to reassign UART ports. We have archived the overlay in zip format and it will need to be uncompressed and copied into the **/boot/overlays** directory on the **SD card**. 

Next we need to edit the /boot/config.txt file by adding the following lines:
```
dtparam=spi=on
dtoverlay=pi3-disable-bt-overlay
core_freq=250
enable_uart=1
force_turbo=1
```
Now edit /boot/cmdline.txt by changing the file to the following:
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```
If you've made changes to the cmdline.txt and config.txt files on your computer, insert the SD card back into your Raspberry Pi 3. Boot the Pi to either a network SSH session or desktop, and execute the following commands in a shell window.

To deactivate the onboard Bluetooth, you must prevent hciattach from attempting to utilize the modem through uart0. This action will disable the corresponding systemd service.
```
sudo systemctl disable hciuart
```
Now edit /lib/systemd/system/hciuart.server and replace ttyAMA0 with ttyS0:
```
sudo nano /lib/systemd/system/hciuart.service
```
Replace ***"After=dev-serial1.device"*** with ***"After=dev-ttyS0.device"***

Use Ctrl+O to save changes and use Ctrl+X to exit.

You should update the operating system by applying the latest patches using:
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```
After your Raspberry Pi 3 completes the reboot process, you should be able to utilize the serial console via the GPIO header at a baud rate of 9600.
For a brief check of the data being transmitted from the GPS, you can enter the following command and then press CTRL+C to exit:
```
sudo cat /dev/ttyS0
```
Run the following two commands to stop and disable the tty service:
```
 sudo systemctl stop serial-getty@ttyS0.service
 sudo systemctl disable serial-getty@ttyS0.service
```
### Reboot 
```
sudo shutdown -r now 
```
### Install GPSD

You can opt to directly read the raw data, but it's more convenient to have Linux software present it in a more readable format. Let's explore gpsd, a GPS-handling Daemon that operates in the background.
To install gpsd, ensure your Pi is connected to the internet, and execute the following commands in the console:
```
sudo apt-get install gpsd gpsd-clients
```
Newer versions of Raspberry Pi OS, starting from "Jessie" onwards, necessitate the deactivation of a service installed by gpsd. This service employs systemd to listen on a local socket and activate gpsd when clients establish a connection. However, it can create conflicts with manually executed gpsd instances, as outlined in this guide. To disable the gpsd systemd service, execute the following commands:
```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```

If there comes a time when you wish to reinstate the default gpsd systemd service, you can use these commands to reactivate it. Keep in mind, however, that the subsequent steps in this guide will no longer be applicable:
```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
```
Edit /etc/default/gpsd as below:
```
sudo nano /etc/default/gpsd
```
change it to look like this
```
START_DAEMON="true"
GPSD_OPTIONS="-n"
DEVICES="/dev/ttyS0"
USBAUTO="false"
GPSD_SOCKET="/var/run/gpsd.sock"
```
Then reboot. 

### Run gpsd
```
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
```

### Test gpsd
Remember that the PI needs clear view of the sky for GPS. There is a simple GPS client which you can run to test if everything is working: 
```
cgps -s 
```

If you encounter issues where cgps consistently shows 'NO FIX' under status and subsequently terminates after a few seconds, you might need to restart the gpsd service. You can achieve this by executing the following commands:
```
 sudo killall gpsd
 sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
```


## Conclusion & future development
We highly recommend to experiment and modify both hardware and software. Maybe clear the code by writing your own libraries or change PiCamera to a different sensor. Feel free to do with this project whatever you want. :)

Probably this project will no longer be supported by us but as we give it to another engineering team it's highly plausible that they would upgrade already existing solutions or add something new. We would try to link their GitHub repos down below: ........
