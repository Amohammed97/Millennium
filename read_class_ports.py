import sys
from serial.serialutil import SerialException
import serial
import time
import glob

## Globale variable ##
ser         = None 
port        = None 
start_bit   = None
end_bit     = None 


class Read():
    # this class contains of 4 methods:
    #     -start()                            this method used to organize which method will execute when the class called
    #     -serial_cheack_configuration()      to check the config.txt file
    #     -serial_configuration()             to display all options of avalibale ports and selected bits to display
    #     -serial_read()                      to display the chosen data in terminal
    # how to use :
    #     - create an object of Read class and call the start method
    # dependencies :
    #     -a config.text file in the same dir of the code *will be auto generated if it's not found*

    def start(self):
        
        if self.serial_cheack_configuration(): #cheack if the config.txt file contain the needed data
                self.serial_read()
        else:
            #this code will enter here if there is no config.txt file        
            try:
                open("config.txt", "x")
            except FileExistsError: # if the file exist but there is a missing parameter just pass to re-configure the file
                pass

            self.serial_configuration()
            self.serial_cheack_configuration() # just to store the new file lines in the global variables
            self.serial_read()

    def serial_cheack_configuration(self):
        
        try:
            
            config = open("config.txt", "r")
            lines  = config.readlines()
        
        except FileNotFoundError: #if the config.txt file dosn't exist return False to creat the file in the start method 
        
            return False

        if len(lines) > 2:
            
            global start_bit
            global end_bit
            global port
            
            try:
            
                start_bit = int(lines[0])
                end_bit   = int(lines[1])
                port      = [lines[2]]
                return True
            
            except ValueError:
        
                self.serial_read() # enter read method to redirect you in configuration method and save it 
        else:
        
            print(" the config.txt file missing a parameter")
            return False

    def serial_read(self):
        
        global start_bit
        global end_bit
        global port
        
        while True:
        
            try:
        
                ser = serial.Serial(
                    port=str(port[0]),\
                    baudrate=9600,\
                    parity=serial.PARITY_NONE,\
                    stopbits=serial.STOPBITS_ONE,\
                    bytesize=serial.EIGHTBITS,\
                    timeout=200)
        
                data = str(ser.read(size=18),encoding='utf-8')
                data = data.replace("#","")
                data = int(data[int(start_bit):int(end_bit)])

                print('weight = '+str(data)+'Kg') #finally print the data
            
            except (TypeError , ValueError): #all errors are expected to face it
        
                print("\nplease re-congifure the device\n")
        
                self.serial_configuration() #force user to re-configure 
                self.serial_cheack_configuration()
                self.serial_read()

            except ( SerialException ):
                self.serial_configuration() #force user to re-configure 
                self.serial_cheack_configuration()
                self.serial_read()

    def serial_configuration(self):
            
            global start_bit
            global end_bit
            global ser
            result = []

            """ Lists serial port names
             :raises EnvironmentError:
            On unsupported or unknown platforms
            :returns:
            A list of the serial ports available on the system in the result  list
             """

            if sys.platform.startswith('win'):
            
                ports = ['COM%s' % (i + 1) for i in range(256)]

            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            
                # this excludes your current terminal "/dev/ttyUSB"
                ports = glob.glob('/dev/ttyUSB*')
            
            else:
            
                raise EnvironmentError('Unsupported platform')
            
            if ports != []:
            
                for port in ports:
            
                    try:
            
                        s = serial.Serial(port)
                        s.close()
                        result.append(port)
                        index = result.index(port)
            
                        print(str(index) + "-" + str(result[index]))
            
                    except (OSError, serial.SerialException): #to exclude unworking ports 
            
                        pass
            
            else:
            
                print("port is not connected please reconnect it")
                time.sleep(5)
                self.serial_read() # call read method because it the method that handle all expected errors and re-run configuration methods again
                #sys.exit() here if i would to exit of the program just need to add logic and counter
            
            confirm_port = input("chose selected port : ") #chose one of ports that desplayed  
           
            try:
            
                ser = serial.Serial(
                    port=str(result[int(confirm_port)]),\
                    baudrate=9600,\
                    parity=serial.PARITY_NONE,\
                    stopbits=serial.STOPBITS_ONE,\
                    bytesize=serial.EIGHTBITS,\
                    timeout=200)
            
            except IndexError: #make sure that enter index port in existing options 
            
                print("You enterd a wrong answer .. please try again")
                self.serial_read() # to re-enter this method and check againg if i still have the smae index error

            data=str(ser.read(size=18),encoding='utf-8') #store the serial data as string with Number of bytes to read
            data=data.replace(" ","#") 
            data_size=len(data)
            
            print(data)
            print("\nselect bites number from 0 to "+str(data_size)+" don't select any bit contain a char\n")

            start_bit = input("Enter your start bit: ")
            end_bit = input("Enter your end bit: ")

            print(data[int(start_bit):int(end_bit)]) 
            print("   Do you want to confirm this configuration   ")

            confirm = input("Enter (Y/y) for yes anything for No : ")

            if confirm == 'Y' or confirm == 'y' :

                #write and save the entered config each one in a separate line
                config = open("config.txt", "w")
                config.write(start_bit+"\n")
                config.write(end_bit+"\n")
                config.write(result[int(confirm_port)])
                config.close()

            else:

                self.serial_configuration() #re-enter the method to do it again
            
if __name__=="__main__":
    
    Balance = Read()
    
    try:

        Balance.start()

    except KeyboardInterrupt:

        print("the program is closed")
    
