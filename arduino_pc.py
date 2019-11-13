s = serial.Serial('COM4',115200,timeout=1) #opens a serial port (resets the device!) time.sleep(2) #give the device some time to startup (2 seconds) 

#write to the device’s serial port 
s.write("a[AB]\n") #set the device address to AB
time.sleep(0.1) #wait for settings to be applied
s.write("c[1,0,5]\n") #set number of retransmissions to 5
time.sleep(0.1) #wait for settings to be applied
s.write("c[0,1,30]\n") #set FEC threshold to 30 (apply FEC to packets with payload >= 30)
time.sleep(0.1) #wait for settings to be applied
s.write("m[hello world!\0,CD]\n") #send message to device with address CD 

#read from the device’s serial port (should be done in a separate thread) 
message = "" 
while True: #while not terminated 
 try: 
   byte = s.read(1) #read one byte (blocks until data available or timeout reached) 
   if byte=='\n': #if termination character reached
     print message #print message
     message = "" #reset message
   else:
     message = message + byte #concatenate the message 
 except serial.SerialException: 
   continue #on timeout try to read again 
 except KeyboardInterrupt: 
   sys.exit() #on ctrl-c terminate program 