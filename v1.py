import serial
import threading
import time
import sys

# Declare portname here
portname = "COM5"

# Enter list of commands. No need to end
# with "\n", it is automatically added.
commands = [
    "p",
    "a[21]",
    "r",
    "a"
]

ser = serial.Serial(port=portname,baudrate=115200,timeout=1)
exitflag = False

# Declare all functions that send to the device here
def tSend():
    for c in commands:
        ser.write(c.rstrip().encode("utf-8"))
        ser.write(b'\n')
        time.sleep(0.1)

def tRecv():
    while not exitflag:
        try:
            msg = ser.readline().decode("utf-8").rstrip()
            if msg != "":
                print(" >> " + msg)
        except serial.SerialException:
            continue

if __name__ == "__main__":
    print("Initialising...")
    time.sleep(2)
    tr = threading.Thread(target=tRecv, daemon=True)
    ts = threading.Thread(target=tSend)
    tr.start()
    ts.start()
    print("Waiting...\n")
    while tr.is_alive() or ts.is_alive():
        try:
            tr.join(1)
            ts.join(1)
        except KeyboardInterrupt:
            print("\nGoodbye")
            sys.exit()
