# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 16:02:32 2025

@author: qpang2
"""

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

import sys,os # system related library
ok_sdk_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\Python\\x64"
ok_dll_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\lib\\x64"
sys.path.append(ok_sdk_loc) # add the path of the OK library
os.add_dll_directory(ok_dll_loc)

import ok,time

dev = ok.okCFrontPanel()
status=dev.OpenBySerial("")
error = dev.ConfigureFPGA("U:\\lens_controller\\lens_controller.runs\\impl_1\\Main.bit")
print(dev.GetDeviceCount())
# It's a good idea to check for errors here!!
 
# IsFrontPanelEnabled returns true if FrontPanel is detected.
if dev.IsFrontPanelEnabled():
     print ("FrontPanel host interface enabled.")
else:
     sys.stderr.write("FrontPanel host interface not detected.")

#%%
print ("send")
for i in range(2000):
    send_double_command(dev,0x0A,0x00)
    # time.sleep(1)
    
send_double_command(dev,0x12,0x80)
# result = reduction(0x8F, 40, 40, 0xF8)
# dev.SetWireInValue(0x00, result)
# dev.UpdateWireIns()
# time.sleep(0.1)
# dev.SetWireInValue(0x00, 0)
# dev.UpdateWireIns()
# time.sleep(0.1)
# print(result)
# dev.ActivateTriggerIn(0x48, result)
# time.sleep(1)
# z=dev.UpdateTriggerOuts()
# z = dev.GetTriggerOutVector(0x60)
# print (z)
#%%
dev.Close