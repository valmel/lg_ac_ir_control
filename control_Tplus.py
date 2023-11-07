import time
import Adafruit_DHT
import logging
import subprocess

logging.basicConfig(filename='tplus5_control.log', level=logging.INFO, format='%(asctime)s, %(message)s')

def execute_system_command(command):
    try:
        subprocess.check_output(command, shell = True)
    except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions
        print(f'Error executing the command: {e}')

# DHT11 sensor connected to GPIO4 -> pin = 4
def tplus5_logic(tobm = False, pin = 4, low_bound_T = 4, upper_bound_T = 10):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    if (temperature < low_bound_T):
        execute_system_command("irsend SEND_ONCE LG_AC ON")
        logging.info(f'{humidity}, {temperature}, ON')
        tobm = True
    if (temperature > upper_bound_T) and (tobm == True):
        execute_system_command("irsend SEND_ONCE LG_AC OFF")
        logging.info(f'{humidity}, {temperature}, OFF')
        tobm = False
    return tobm

turned_on_by_me = False
while True:
    turned_on_by_me = tplus5_logic(turned_on_by_me)
    time.sleep(300)
