import numpy as np
import struct
import tkinter as tk
from tkinter import messagebox
def reduction(val1, delay1, delay2, val2=0):
    SPI_control = (val1 << 24) | (delay1 << 17) | (0x00<<16) | (val2 << 8) | (delay2 << 1) | 0x01
    return SPI_control
    
# def send_single_command(dev, val1):
#     result = reduction(val1, 40, 40, 0)
#     dev.SetWireInValue(0x00, result)
#     dev.UpdateWireIns()
#     time.sleep(0.1)
#     dev.SetWireInValue(0x00, 0)
#     dev.UpdateWireIns()
#     time.sleep(0.1)
    
def send_double_command(dev, val1, val2):
    result = reduction(val1, 80, 80, val2)
    dev.SetWireInValue(0x00, result)
    dev.UpdateWireIns()
    # time.sleep(0.01)
    dev.SetWireInValue(0x00, 0)
    dev.UpdateWireIns()
    # time.sleep(0.01)
    
def send_single_command(dev,val1):
    result = reduction(0x00, 80, 80, val1)
    dev.SetWireInValue(0x00, result)
    dev.UpdateWireIns()
    # time.sleep(0.01)
    dev.SetWireInValue(0x00, 0)
    dev.UpdateWireIns()
    # time.sleep(0.01)
    
def getDLC(dev):
    dev.UpdateWireOuts()
    return dev.GetWireOutValue(0x20)
def focus_max(dev):
    send_single_command(dev, 0x05)

def focus_min(dev):
    send_single_command(dev, 0x06)

def get_lens_name(dev):
    lens_name = ""
    send_single_command(dev, 0x82)
    
    send_single_command(dev, 0x83)
    DLC = getDLC(dev)
    while(DLC != 0):
        lens_name = lens_name + chr(DLC)
        send_single_command(dev, 0x83)
        DLC = getDLC(dev)
    return lens_name

def change_aperature(dev, increment):
    if(increment < 0):
        increment += 256
    send_single_command(dev, 0x13)
    send_single_command(dev, (increment))
    
def change_focus(dev, increment):
    if(increment < 0):
        increment += 65535
    HH = increment >> 8
    LL = increment & 255
    send_single_command(dev, 0x44)
    send_single_command(dev, HH)
    send_single_command(dev, LL)
#%%
import sys,os # system related library
ok_sdk_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\Python\\x64"
ok_dll_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\lib\\x64"
sys.path.append(ok_sdk_loc) # add the path of the OK library
os.add_dll_directory(ok_dll_loc)

import ok,time
#%%
dev = ok.okCFrontPanel()
status=dev.OpenBySerial("")
error = dev.ConfigureFPGA("..\\lens_control.runs\\impl_1\\Main.bit")
print(dev.GetDeviceCount())
# It's a good idea to check for errors here!!
 
# IsFrontPanelEnabled returns true if FrontPanel is detected.
if dev.IsFrontPanelEnabled():
     print ("FrontPanel host interface enabled.")
else:
     sys.stderr.write("FrontPanel host interface not detected.")

#%%
print ("init lens")
for i in range(50):
    send_single_command(dev,0x0A)
    #time.sleep(0.01)

#%%


# change_aperature(dev, -10)
# change_focus(dev, 1000)

# send_single_command(dev, 0x00)
# send_single_command(dev, 0x91)
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))
# send_single_command(dev, 0x00)
# print(chr(getDLC(dev)))
# print(hex(getDLC(dev)))
# print(int(getDLC(dev)))




#%%
# value = int("0028", 16)
# packed = struct.pack('H', value)  # 'h' is the format code for int16
# float16_value = struct.unpack('e', packed)[0]  # 'e' is the format code for float16 (half-precision)
# print(float16_value)
print(int(0xFF))


#%%
dev.Close