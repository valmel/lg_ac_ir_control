import time
import Adafruit_DHT
import schedule
import logging

logging.basicConfig(filename='temp_and_humidity.log', level=logging.INFO, format='%(asctime)s, %(message)s')

# DHT11 sensor connected to GPIO4 -> pin = 4
def get_temp_and_hum(pin = 4):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    logging.info(f'{humidity}, {temperature}')

#schedule.every(10).seconds.do(get_temp_and_hum)
schedule.every(1).minutes.do(get_temp_and_hum)
#schedule.every().hour.do(get_temp_and_hum)

while True:
    schedule.run_pending()
    time.sleep(60)
