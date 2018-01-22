import RPi.GPIO as GPIO
import threading
import dht11
import time

h_dht = -1
t_dht = -1

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
# So I thread the reading updating the global vars
class ReadDHT(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global h_dht
        global t_dht
        while True:
            instance = dht11.DHT11(pin = 12)
            result = instance.read()
            if result.is_valid():
                t_dht = result.temperature
                h_dht = result.humidity
            time.sleep(1)


def initialize():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([11], GPIO.OUT)
    GPIO.setup([12], GPIO.IN)
    GPIO.output(11, 1)
    dht_thread = ReadDHT()
    dht_thread.start()

def lights_on():
    GPIO.output(11, 0)

def lights_off():
    GPIO.output(11, 1)

def lights_status():
    if GPIO.input(11) == 0 :
        return "on"
    else:
        return "off"

def fan_status():
    return "off"

def h1_status():
    global h_dht
    return h_dht

def t1_status():
    global t_dht
    return t_dht
