import serial
import threading 
import logging
import time

# Settings for serial port
SERIAL_PORT = "COM5"
SERIAL_BAUDRATE = 9600 

def openSerialPort(portName, baudrate): 
    try :
        serialDevice = serial.Serial(port=portName,
                                    baudrate=baudrate,
                                    parity=serial.PARITY_NONE
                                    )
    except:
        print("Device {} not found" .format(portName))
        exit()
    return serialDevice

def threadRead(serialDevice):
    while(1):
        readString = serialDevice.read()
        logging.info("Read string: %s\n", readString)
        logging.info("Read thread\n")
        time.sleep(1)

if __name__ == "__main__":
    # Initialize logging settings 
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    serialDevice = openSerialPort(SERIAL_PORT, SERIAL_BAUDRATE)
    # Initialize read thread for reading responses
    retReadThread = threading.Thread(target=threadRead, daemon=True, args=(serialDevice))
    retReadThread.start()

    #Main thread to write AT commands
    while(1): 
        logging.info("Main thread\n")
        serialDevice.write(b'AT\r')
        time.sleep(1)
        