import RPi.GPIO as GPIO
import Adafruit_DHT
from flask import Flask, render_template, request, redirect, url_for
import subprocess

application = Flask(__name__)

sensor_pin = 4  # GPIO pin for DHT11

#GPIO.setmode(GPIO.BCM)

def execute_system_command(command):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions
        print(f"Error executing the command: {e}")

@application.route("/", methods=["GET", "POST"])
def index():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor_pin)
    return render_template("index.html", temperature=temperature, humidity=humidity)

@application.route("/button", methods=["POST"])
def button_action():
    if request.method == "POST":
        button_action = request.form["action"]
        if button_action == "on":
            execute_system_command("irsend SEND_ONCE LG_AC ON")
        elif button_action == "off":
            execute_system_command("irsend SEND_ONCE LG_AC OFF")
    return redirect(url_for("index"))

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
