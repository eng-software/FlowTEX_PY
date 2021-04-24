''' 
  TexNet.py

    Created: 23/04/2021 12:30:00
    Author: henrique.coser

   This example code is in the Public Domain

   This software is distributed on an "AS IS" BASIS, 
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
   either express or implied.

   Este código de exemplo é de uso publico,

   Este software é distribuido na condição "COMO ESTÁ",
   e NÃO SÃO APLICÁVEIS QUAISQUER GARANTIAS, implicitas 
   ou explicitas

'''
import serial, os, time, serial.tools.list_ports
import Chronometer
import struct


class TexNet:
    #--------------------------------------------
    def __init__(self, serialPort):
        self.rxTimer = Chronometer.Chronometer()        
        self.opcode = 0
        self.length = 0
        self.Data = []
        self.newFrame = False        
        self.error = False
        self.ser = serial.Serial(serialPort, 115200, timeout = 0)
        if(self.ser.isOpen() == False):
            self.ser.open()
    #--------------------------------------------
    # STATE MACHINE - STX
    #--------------------------------------------
    def waitSTX(self, data):
        value = int.from_bytes(data, "big")
        if( value == 0x02):
            self.mstate = self.waitOpcode
            self.rxTimer.restart()
    #--------------------------------------------
    # STATE MACHINE - OPCODE
    #--------------------------------------------
    def waitOpcode(self, data):
        self.opcode = int.from_bytes(data, "big")
        self.mstate = self.waitLength
        self.rxTimer.restart()
    #--------------------------------------------
    # STATE MACHINE - LENGTH
    #--------------------------------------------
    def waitLength(self, data):
        self.length = int.from_bytes(data, "big")
    
        self.Data.clear()
    
        if(self.length == 0):
            self.mstate = self.waitChks
        else:
            self.mstate = self.waitData        
    
        self.rxTimer.restart()
    #--------------------------------------------
    # STATE MACHINE - DATA
    #--------------------------------------------
    def waitData(self, data):
        self.Data.append( int.from_bytes(data,"big") )
    
        if(len(self.Data) >= self.length):
            self.mstate = self.waitChks

        self.rxTimer.restart()
    #--------------------------------------------
    # STATE MACHINE - CHECKSUM
    #--------------------------------------------
    def waitChks(self, data):
        calcChks = self.opcode + self.length;

        for value in self.Data:
            calcChks += value

        calcChks = calcChks & 0xFF
    
        if(calcChks == int.from_bytes(data, "big")):
            self.newFrame = True
            self.error = False
        else:
            self.newFrame = False
            self.error = True
            print("Frame error")

        self.mstate = self.waitSTX

        self.rxTimer.restart()
    #--------------------------------------------
    # PROCESS STATE MACHINE
    #   Get the data received from serial and process
    #   the state machine
    #--------------------------------------------
    def processData(self, data):        
        self.mstate(data)
    #--------------------------------------------
    # Request to slave
    #   Send a request
    #       Input:  The request opcode
    #       Output:
    #           On Success: list of received dara
    #           On error: None
    #--------------------------------------------
    def request(self, requestOpcode):
        if(type(requestOpcode) is not int):
            requestOpcode = int.from_bytes(requestOpcode, "big")

        #Build request frame: STX + OPCODE + LENGTH + CHKS
        reqFrame = [0x02, requestOpcode, 0, requestOpcode]
        
        #Clear remaining data
        self.error = False
        self.newFrame = False
        self.rxTimer.restart()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(reqFrame)
        self.mstate = self.waitSTX

        #Will poll the serial until get error, a response frame or timeout
        while((self.rxTimer.getElapsed() < 2)and(self.newFrame == False)and(self.error == False)):
            if(self.ser.in_waiting > 0):
                value = self.ser.read(1)
                self.processData(value)

        if(self.newFrame):
            return self.Data
        else:
            return None
    #--------------------------------------------
    # Request a version 
    #       Output:
    #           On Success: Version string
    #           On error: None
    #--------------------------------------------
    def getVersion(self):        
        value = self.request(0x76)
        
        if(value is not None):
            strValue = ''.join(chr(e) for e in value)
            return strValue

        return None
    #--------------------------------------------
    # Request a flow value 
    #       Output:
    #           On Success: float of the value
    #           On error: float 0.0
    #--------------------------------------------
    def getFlow(self):        
        value = self.request(0x46)
        
        if(value is not None):
            flowData = bytearray(value[0:4])
            tempData = bytearray(value[4:8])
            fV = struct.unpack('f',flowData)[0]
            tV = struct.unpack('f',tempData)[0]
            return fV

        return 0.0
    #--------------------------------------------
    # Request a temperature
    #       Output:
    #           On Success: float of temperature
    #           On error: None
    #--------------------------------------------
    def getTemperature(self):        
        value = self.request(0x46)
        
        if(value is not None):
            flowData = bytearray(value[0:4])
            tempData = bytearray(value[4:8])
            fV = struct.unpack('f',flowData)[0]
            tV = struct.unpack('f',tempData)[0]
            return tV

        return 0.0
    #--------------------------------------------
    # Request a serial number
    #       Output:
    #           On Success: string of the serial number
    #           On error: None
    #--------------------------------------------
    def getSerialNumber(self):        
        value = self.request(0x6E)
        
        if(value is not None):
            strValue = ''.join(chr(e) for e in value)
            return strValue

        return None
    #--------------------------------------------
    # Request a model
    #       Output:
    #           On Success: string of the model
    #           On error: None
    #--------------------------------------------
    def getModel(self):        
        value = self.request(0x6D)
        
        if(value is not None):
            strValue = ''.join(chr(e) for e in value)
            return strValue

        return None
    #--------------------------------------------

    #State machine variable 
    mstate = waitSTX