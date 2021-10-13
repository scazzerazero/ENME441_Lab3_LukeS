#   To check address: sudo i2cdetect -y 1

import smbus
import time

class PCF8591:

  def __init__(self,address): #the eslf has attritubtes. Here it only has one.
    #self.___ represents the instance of the class. By using the “self” keyword we can access the attributes and methods of the class in python. It binds the attributes with the given arguments. The reason you need to use self. is because Python does not use the @ syntax to refer to instance attributes.
    self.bus = smbus.SMBus(1) #newer Pis use bus no.1
    self.address = address #the I2C device lives at a address in the bus
  #the self can do things! Creating our read() and write() methods:
  def read(self,chn): #channel
      try:
          # Read/write 1 byte from/to a specific register of a given device address
          #note about the control byte for ADC:
            #0,analog out enabled?,analog in channel select,analog in channel select,0,A/D channel number 0 1 2 or 3
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000

          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))



class Joystick:
  def __init__(self,address):
    self.ADC=PCF8591(address)

  def getX(self):
    return PCF8591.read(1) #read channel one
  def getY(self):
    return PCF8591.read(2) #read channel two

JoystickObject=Joystick(0x48)
while 1:
  try:
    print("{:>3},{:>3}".format(JoystickObject.getX(), JoystickObject.getY())) #thanks gavin and hannah!
    time.sleep(0.1)
  except:
    KeyboardInterrupt
    print("cancelled!")




