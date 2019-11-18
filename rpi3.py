#
# Testing purpose only. This python script is socketio
# client that receives a request (EXECUTE intent) and
# perform an action in the physical device.
#

import socketio
import RPi.GPIO as GPIO
import logging
import json

logging.basicConfig(level=logging.DEBUG)
sio = socketio.Client()
#initial GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

@sio.event
def connect():
    print('Connection Established!')

@sio.event
def message(data):
    print('Message received with ', data)

@sio.on('REQUEST')
def on_json(data):
    print('Received Assistant request: ', data)
    sio.emit('RESPONSE', {"status": 200})

    # identify the device
    if (data["id"] == '1emw'):
        logging.info('Table Lamp')
    elif (data["id"] == 'p5e'):
        logging.info('Daddy Lamp')
    elif (data["id"] == '1ris'):
        logging.info('Ceilling lamp')
    elif (data["id"] == 'spf'):
        logging.info('Thermostat')

    # GPIO action
    # Workaround: Turn on/off is not mapped
    # to a specific device. On/Off request
    # to any device will change the LED status.
    if (data["params"]["on"] == True):
        logging.info('Turning LED on')
        GPIO.output(17,1)
    elif (data["params"]["on"]  == False):
        logging.info('Turning LED off')
        GPIO.output(17,0)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://35.196.128.192:3001')

sio.wait()
