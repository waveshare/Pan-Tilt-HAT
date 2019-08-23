#!/usr/bin/python

import time
import math
import smbus
import pygame

COMMAND_CMD  = 0x80   
TRANSACTION  = 0x40    # Read/Write block protocol.
TRANSACTION_SPECIAL = 0X60

#address
CONTROL   	= 0x00
TIMING    	= 0x01
INTERRUPT 	= 0X02
THLLOW 		= 0x03
THLHIGH 	= 0X04
THHLOW 	    = 0x05
THHHIGH     = 0X06
ANALOG 	    = 0X07

ID 		    = 0X12
DATA0LOW    = 0X14
DATA0HIGH   = 0X15
DATA1LOW    = 0X16
DATA1HIGH 	= 0X17
#---------------------------------------------------
ADC_EN			  = 0X02
CONTROL_POWERON   = 0x01
CONTROL_POWEROFF  = 0x00
INTR_TEST_MODE 	  = 0X30
INTR_INTER_MODE   = 0X18#At least 8 cycles to stabilize, otherwise the interrupt will continue to maintain 0 

#transaction_special
SPECIAL_FUN_RESER1 	  = 0X00
SPECIAL_FUN_INTCLEAR  = 0X01
SPECIAL_FUN_STOPMAN   = 0X02
SPECIAL_FUN_STARTMAN  = 0X03
SPECIAL_FUN_RESER2 	  = 0X0F

#interrupt
INTEGRATIONTIME_Manual    = 0x00
INTEGRATIONTIME_2Z7MS 	  = 0xFF
INTEGRATIONTIME_5Z4MS 	  = 0xFE
INTEGRATIONTIME_51Z3MS    = 0xED
INTEGRATIONTIME_100MS 	  = 0xDB
INTEGRATIONTIME_200MS 	  = 0xB6
INTEGRATIONTIME_400MS     = 0x6C
INTEGRATIONTIME_688MS 	  = 0x01

#analog
GAIN_1X   = 0x00
GAIN_8X   = 0x01
GAIN_16X  = 0x02
GAIN_111X = 0x03


LUX_SCALE     = 16 # scale by 2^16
RATIO_SCALE   = 9  # scale ratio by 2^9
#---------------------------------------------------
# Integration time scaling factors
#---------------------------------------------------
CH_SCALE =16 # scale channel values by 2^16

# Nominal 400 ms integration. 
# Specifies the integration time in 2.7-ms intervals
# 400/2.7 = 148
NOM_INTEG_CYCLE = 148
#---------------------------------------------------
# Gain scaling factors
#---------------------------------------------------
CH0GAIN128X = 07 # 128X gain scalar for Ch0
CH1GAIN128X = 115 # 128X gain scalar for Ch1

#---------------------------------------------------
K1C = 0x009A # 0.30 * 2^RATIO_SCALE
B1C = 0x2148 # 0.130 * 2^LUX_SCALE
M1C = 0x3d71 # 0.240 * 2^LUX_SCALE

K2C = 0x00c3 # 0.38 * 2^RATIO_SCALE
B2C = 0x2a37 # 0.1649 * 2^LUX_SCALE
M2C = 0x5b30 # 0.3562 * 2^LUX_SCALE

K3C = 0x00e6 # 0.45 * 2^RATIO_SCALE
B3C=  0x18ef # 0.0974 * 2^LUX_SCALE
M3C = 0x2db9 # 0.1786 * 2^LUX_SCALE

K4C = 0x0114 # 0.54 * 2^RATIO_SCALE
B4C = 0x0fdf # 0.062 * 2^LUX_SCALE
M4C = 0x199a # 0.10 * 2^LUX_SCALE

K5C = 0x0114 # 0.54 * 2^RATIO_SCALE
K5C = 0x0114 # 0.54 * 2^RATIO_SCALE
B5C = 0x0000 # 0.00000 * 2^LUX_SCALE
M5C = 0x0000 # 0.00000 * 2^LUX_SCALE

class TSL2581:
  def __init__(self, address=0x39, debug=False):
    self.i2c = smbus.SMBus(1)
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting TSL2581")

  def Write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.i2c.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
	  
  def Read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.i2c.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result
          
  def Init_TSL2581(self):
    print("****** init TSL2581 ******")
    self.Write(COMMAND_CMD | CONTROL, CONTROL_POWERON)
    time.sleep(2)
    self.Write(COMMAND_CMD | TIMING, INTEGRATIONTIME_400MS)
    self.Write(COMMAND_CMD | CONTROL, ADC_EN | CONTROL_POWERON)
    self.Write(COMMAND_CMD | INTERRUPT, INTR_INTER_MODE)
    self.Write(COMMAND_CMD | ANALOG, GAIN_8X )

  def Read_ID(self):
    id = self.Read(COMMAND_CMD | TRANSACTION | ID)
    return id

  def SET_Interrupt_Threshold(self, min, max):
    DataLLow = min % 256
    DataLHigh = min / 256
    self.Write(COMMAND_CMD | THLLOW, DataLLow)
    self.Write(COMMAND_CMD | THLHIGH, DataLHigh)

    DataHLow = max % 256
    DataHHigh = max / 256
    self.Write(COMMAND_CMD | THHLOW, DataHLow)
    self.Write(COMMAND_CMD | THHHIGH, DataHHigh)

  def Read_Channel(self, Channel):
    if (Channel == 0):
      DataLow  = self.Read(COMMAND_CMD | TRANSACTION | DATA0LOW)
      DataHigh = self.Read(COMMAND_CMD | TRANSACTION | DATA0HIGH) 

    elif (Channel == 1):
      DataLow  = self.Read(COMMAND_CMD | TRANSACTION | DATA1LOW)
      DataHigh = self.Read(COMMAND_CMD | TRANSACTION | DATA1HIGH)     
    value = 256 * DataHigh + DataLow 
    return value

  def calculate_Lux(self, iGain=1, tIntCycles=NOM_INTEG_CYCLE):
    if (tIntCycles == NOM_INTEG_CYCLE):
      chScale0 = (1 << (CH_SCALE))
    elif (tIntCycles != NOM_INTEG_CYCLE):
      chScale0 = (NOM_INTEG_CYCLE << CH_SCALE) / tIntCycles 

    if (iGain == 0):
      chScale1 = chScale0
    elif (iGain == 1):
      chScale0 = chScale0 >> 3; # Scale/multiply value by 1/8
      chScale1 = chScale0;
    elif (iGain == 2):
      chScale0 = chScale0 >> 3; # Scale/multiply value by 1/16
      chScale1 = chScale0;
    elif (iGain == 3):
	  chScale1 = chScale0 / CH1GAIN128X
	  chScale0 = chScale0 / CH0GAIN128X
    
    Channel_0 = self.Read_Channel(0)
    Channel_1 = self.Read_Channel(1)
    channel0 = (Channel_0 * chScale0) >>  CH_SCALE
    channel1 = (Channel_1 * chScale1) >>  CH_SCALE

    ratio1 = 0
    if (channel0 != 0):
      ratio1 = (channel1 << (RATIO_SCALE + 1)) / channel0
    ratio = (ratio1 + 1) >> 1
    
    if ((ratio >= 0X00) or (ratio <= K1C)):
      b = B1C  
      m = M1C
    elif(ratio <= K2C):
      b = B2C  
      m = M2C
    elif (ratio <= K3C):
      b = B3C
      m = M3C
    elif (ratio <= K4C):
      b = B4C
      m = M4C
    elif (ratio > K5C):
      b = B5C
      m = M5C

    temp = ((channel0 * b) - (channel1 * m))
    temp = temp+(1 << (LUX_SCALE - 1))			

    lux_temp = temp >> LUX_SCALE			
    return lux_temp





