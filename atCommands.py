import serial
import threading 
import logging
import time
import argparse

# Settings for serial port
SERIAL_PORT = "COM9"
SERIAL_BAUDRATE = 38400 

def openSerialPort(portName, baudrate): 
    try :
        serialDevice = serial.Serial(port=portName,
                                    baudrate=baudrate,
                                    parity=serial.PARITY_NONE
                                    )
    except:
        print("Device {} could not be opened" .format(portName))
        exit()
    print("Device: {} opened" .format(portName))
    return serialDevice

def parserInit():
    parser = argparse.ArgumentParser(prog='AT cmds tool',
                                     description='Send AT commands to ESP8266 deice'
                                     )
    parser.add_argument('cmd', type=str, help='Command to be sent')
    return parser


def processCmd(cmd):
    logging.info("Command: %s\n", cmd)

    # Write AT command
    if (cmd == "test"):
        serialDevice.write(b'AT\r\n')

    # Read response 
    lineRead = serialDevice.readline()
    if lineRead:
        line = lineRead.decode()
        print(line)

if __name__ == "__main__":
    # Initialize logging settings 
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    serialDevice = openSerialPort(SERIAL_PORT, SERIAL_BAUDRATE)
    # Initialize command line parser
    parser = parserInit()

    while(1):
        args = parser.parse_args()
        processCmd(args.cmd)
        serialDevice.close()
        logging.info("Program finished\n")
        exit()
