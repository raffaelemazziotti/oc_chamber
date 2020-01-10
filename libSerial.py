
import serial
import sys
import glob
from serial.tools import list_ports
import time

# LOW LEVEL ARDUINO COMMUNICATION 

def connect(port=None,baud=9600):
    if port is None:
        obj = ports()
        port = obj[0] # CONNECTS AUTOMATICALLY WITH THE FIRST SERIAL PORT
        
    connection = serial.Serial(port,baud,bytesize=8, parity='N', stopbits=1, timeout=None, rtscts=0)  # open serial port
    time.sleep(3)
    return connection
        
def disconnect(connection):
    connection.close()
    
def write(connection,string):
    connection.write(bytes(string,'UTF-8'))
    connection.flush()

def readline(connection):
    return connection.readline() # read a '\n' terminated line 
    
    
def wait(connection,timeout=10):
    start_time = time.time()
    while connection.in_waiting==0:
        if (time.time() - start_time)>=timeout:
            return False
        time.sleep(.01)
        
    return True

def infWait(connection):
    while connection.in_waiting==0:
        time.sleep(.01)
        
def flushInput(connection):
    connection.flushInput()
def flushOutput(connection):
    connection.flushOutput()
def flush(connection):
    connection.flush()

def ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



#===============================================================================
if __name__=="__main__":
    con = connect()
    # 
    write(con,bytes('30','UTF-8'))
    print('Waiting for incoming data...')
    b =wait(con)
    if(b):
        print(readline(con))
    else:
        print('Timeout reached: No data to print')
     
    disconnect(con)
#===============================================================================


