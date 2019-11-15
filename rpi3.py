import socketio
import RPi.GPIO as GPIO
import logging
import json


sio = socketio.Client()
# initial GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)


@sio.event
def connect():
    print('socket.io established')

@sio.event
def message(data):
    print('Message:', data)

@sio.on('REQUEST')
def onrequest(param):
    print('Assistant request:', param)
    sio.emit('RESPONSE', {"status": 200})

    if (param["params"]["on"] == True):
        logging.info('Turning led on')
        GPIO.output(17,1)
    elif (param["params"]["on"]  == False):
        logging.info('Turning led off')
        GPIO.output(17,0)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://35.196.128.192:3001')

sio.wait()
