LG AC Infrared Remote Control
=============================

LG split AC units W09EG.NSJ + W09EG.UA3 without a Wi-Fi option are controled via LIRC.
First ON/OFF buttons of AKB74955603 remote are mapped using mode2, since irrecord does not work.
The conf file can be prepared from the raw output of mode2 using this [notebook](/notebooks/mode2_to_conf.ipynb). The resulting [conf file](/system_files/LG_AC.lircd.confd) should be coppied to /etc/lirc/lircd.conf.d directory.

Hardware:

1. [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) (or use version 2).
2. [DHT11](https://www.az-delivery.de/en/products/dht-11-temperatursensor-modul) sensor.
3. [USB IR Toy v2](http://dangerousprototypes.com/docs/USB_IR_Toy_v2). This one is not available anymore. But to read or send IR signals with RP is easy. Use e.g. this [receiver](https://www.seeedstudio.com/Grove-Infrared-Receiver.html) and this [transmitter](https://wiki.seeedstudio.com/Grove-Infrared_Emitter/).

An automatic anti-freeze control is implemented [here](control_Tplus.py) and the logging of temperature and humidity from DHT11 sensor [here](logging_dht11.py).

Both scripts are run at reboot using cron. Use

    crontab -e
and add these two lines:

    @reboot /usr/bin/python /path/to/logging_dht11/logging_dht11.py > /tmp/logging_dht11_cron.log 2>&1
    @reboot /usr/bin/python /path/to/control_Tplus/control_Tplus.py > /tmp/control_Tplus_cron.log 2>&1

where you supply your path to the scripts. It is also advisable to use cron to reboot the Raspberry Pi Zero regularly, for example, once a month.

Moreover, I have implemented a minimalistic Flask-based remote control [web app](/lg_remote). After instalation, it is accesible locally at https://hostname.local, where hostname is your Raspberry Pi Zero hostname.

To make it run:

Copy the files somewhere in your home directory. Then make sure that Apache and mod_wsgi are installed on your Raspberry Pi. You can install them using the following command:

    sudo apt-get update
    sudo apt-get install apache2 libapache2-mod-wsgi-py3

Enable mod_wsgi:

    sudo a2enmod wsgi

Copy and adapt the configuration [file](/system_files/lg_webapp.conf) to /etc/apache2/sites-available and enable the virtual host:

    sudo a2ensite lg_webapp

Disable the default Apache webpage:

    sudo a2dissite 000-default

Restart Apache:

    sudo systemctl restart apache2

If you encounter errors, please check the log:

    cat /var/log/apache2/error.log

Give me feedback if you wish or let me know if you need some help.
