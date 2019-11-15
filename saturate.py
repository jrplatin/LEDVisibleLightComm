import serial
import threading
import time
import sys

# Declare portname here
portname = "COM5"

# Enter list of commands. No need to end
# with "\n", it is automatically added.
commands = [
    "r",
    "a[AA]",
    "c[1,0,5]",
    "c[0,1,30]",
]

ser = serial.Serial(port=portname,baudrate=115200,timeout=1)
exitflag = False
debugflag = True
payloadsize = 1
destaddr = "01"
rdytosend = True
mutex = threading.Lock()

# Declare all functions that send to the device here
def tSend():
    global rdytosend
    for c in commands:
        ser.write(c.rstrip().encode("utf-8"))
        ser.write(b'\n')
        time.sleep(0.1)
    while not exitflag:
        if rdytosend:
            ser.write(_to_sending_string("A"*payloadsize).rstrip().encode("utf-8"))
            ser.write(b'\n')
            mutex.acquire()
            try:
                rdytosend = False
            finally:
                mutex.release()
        time.sleep(0.01)

def _to_sending_string(str_to_send):
    return "m[" + str_to_send + "\0," + destaddr + "]"


def tRecv():
    global rdytosend
    while not exitflag:
        try:
            msg = ser.readline().decode("utf-8").rstrip()
            if msg != "" and (msg.startswith("m[R,D")):
                # print(" >> " + msg)
                print(msg.split(",")[2][:-1])
            elif msg != "" and debugflag:
                print(msg)
                if msg == "m[D]":
                    mutex.acquire()
                    try:
                        rdytosend = True
                    finally:
                        mutex.release()
        except serial.SerialException:
            continue

if __name__ == "__main__":
    print("Initialising...")
    time.sleep(2)
    tr = threading.Thread(target=tRecv, daemon=True)
    ts = threading.Thread(target=tSend, daemon=True)
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
