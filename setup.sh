#=================================
FOR THE FIRST RUN
source_directory=$(pwd)

if [ $(uname -m) == armv7l ];then
       echo "You have 32bit architecture, which means it matches for this program"
       # Three lines below are responsible for  installing the WiringPi library
       cd /tmp
       wget https://unicorn.drogon.net/wiringpi-2.46-1.deb
       sudo dpkg -i wiringpi-2.46-1.deb
else
       echo "You have 64bit architecture, which is not match for this program"
       echo "Please install 32bit OS architecture."
       exit 0
fi

cd ${source_directory}

sudo raspi-config nonint do_spi 0

if [ ! -d "$venv" ]; then
       python3 -m venv venv
fi

source ./venv/bin/activate

pip3 install RPi.GPIO
pip3 install picamera
pip3 install Pillow

deactivate
#=================================
