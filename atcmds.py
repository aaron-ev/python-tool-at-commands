import serial
import argparse

DEFAULT_PORT = "COM9"
DEFAULT_BAUDRATE = 38400
DEFAULT_CMD = "test"
DEFAULT_TIMEOUT = 1
baudratesSupported = {
                        4800,
                        9600, 
                        19200, 
                        38400, 
                        57600, 
                        115200, 
                        230400, 
                        460800, 
                        921600, 
                        1382400,
                        }

def openSerialPort(portName, baudrate): 
    try :
        serialDevice = serial.Serial(port=portName,
                                     baudrate=baudrate,
                                     parity=serial.PARITY_NONE,
                                     timeout=DEFAULT_TIMEOUT
                                     )
    except:
        print("Device {} could not be opened" .format(portName))
        exit()
    print("Device: {} opened, baudrate: {}" .format(portName, baudrate))
    return serialDevice

def parserInit():
    parser = argparse.ArgumentParser(prog='AT cmds tool',
                                     description= "Tool to send basic AT commands for managing bluetooth HC-0x devices"
                                     )
    parser.add_argument("cmd", type=str, help="Command to run", default=DEFAULT_CMD, nargs="+")
    parser.add_argument("-b", "--baudrate", type=str, help="Serial port baudrate", default=DEFAULT_BAUDRATE)
    parser.add_argument("-p", "--port", type=str, help="Serial port device", default=DEFAULT_PORT)
    parser.add_argument("-w", "--write", help="Write operation", nargs="+")
    parser.add_argument("-r", "--read", help="Read operation", action= "store_true")
    return parser

def sendCmd(cmd):
    cmd = cmd + '\r\n'
    serialDevice.write(cmd.encode('utf-8'))

def processArgs(args):
    # print(args)
    cmd = args.cmd[0]
    print("Command = {}, arguments = {}" .format(cmd, args.write))

    # Command processing
    if cmd == "test":
        sendCmd("AT")
    elif cmd == "name":
        sendCmd("AT+NAME")
    elif cmd == "uart":
        if not(args.write):
            sendCmd("AT+UART")
        else:
            newBaudrate = int(args.write[0])
            if newBaudrate in baudratesSupported:
                # UART is set to: new baudrate, no parity bit, stop bits = 1
                # by default
                sendCmd("AT+UART=" + str(newBaudrate) + ",0,0")
            else:
                print("Baudrate not supported: {}" .format(newBaudrate))
    elif cmd == "password":
        if not(args.write):
            sendCmd("AT+PSWD")
        else:
            newPassword = args.write[0]
            sendCmd("AT+PSWD=" + newPassword)
    elif cmd == "state":
        sendCmd("AT+STATE")
    elif cmd == "readmode":
        #TODO
        pass

    # Read response 
    lineRead = serialDevice.readline()
    if lineRead:
        line = lineRead.decode()
        print("Response: {}" .format(line))
    else:
        print("AT device did not response in {}s" . format(DEFAULT_TIMEOUT))

if __name__ == "__main__":
    # Initial setup 
    parser = parserInit()
    args = parser.parse_args()
    serialDevice = openSerialPort(args.port, args.baudrate)

    while(1):
        processArgs(args)
        serialDevice.close()
        exit()
