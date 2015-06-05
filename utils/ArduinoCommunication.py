import serial

__author__ = 'fums'


class ArduinoCommunication(object):
    def __init__(self, usbPort, baudrate):
        self._usbPort = usbPort
        self._baudrate = baudrate
        self._arduino = serial.Serial(self._usbPort, self._baudrate)

    def sendToIno(self, data):
        self._arduino.write(str(data))