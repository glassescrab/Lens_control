import numpy as np
import struct
from tkinter import *
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
    
def printval(val):
    print(val)

class LensController:
    def __init__(self,dev):
        self.focus_level = 1
        self.aperature_level = 1
        self.dev = dev
        self.name = ""
       
        
    def initializeLens(self):
        for i in range(50):
            send_single_command(self.dev,0x0A)
        time.sleep(0.1)
        self.resetLens()
        time.sleep(0.1)
        self.getName()
        
            
    def resetLens(self):
        self.aperature_level = 1
        self.focus_level = 1
        change_aperature(self.dev, -127)
        time.sleep(0.5)
        change_focus(self.dev, 32767)
        # self.changeAperature(1)
        # self.changeFocus(1)
        
    def changeFocus(self, new_level=0):
        if(new_level < 1 or new_level > 10):
            return
        difference_level = -1*(new_level - self.focus_level)
        change_focus(self.dev, int(difference_level / 10 * 2100))
        self.focus_level = new_level
        return
    
    def changeAperature(self, new_level = 0):
        if(new_level < 1 or new_level > 10):
            return
        difference_level = new_level - self.aperature_level
        change_aperature(self.dev, int(difference_level / 10 * 64))
        self.aperature_level = new_level
        return
       
    def sync(self, new_focus_level=0, new_aperature_level=0):
        self.changeFocus(new_focus_level)
        time.sleep(0.2)
        self.changeAperature(new_aperature_level)
        return
    
    def getName(self):
        self.name = get_lens_name(self.dev)
        return 
        
    def printName(self):
        print(self.name)
        return


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Persistent Object GUI")
        
        # Instantiate the object and keep it throughout the session
        self.my_object = MyObject("SessionObject")
        
        self.label = tk.Label(root, text=self.my_object.get_info(), font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.increment_button = tk.Button(root, text="Increment", command=self.increment_counter)
        self.increment_button.pack(pady=5)
        
        self.show_button = tk.Button(root, text="Show Info", command=self.show_info)
        self.show_button.pack(pady=5)
    
    def increment_counter(self):
        self.my_object.increment()
        self.label.config(text=self.my_object.get_info())
    
    def show_info(self):
        messagebox.showinfo("Object Info", self.my_object.get_info())


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

    

lens = LensController(dev)
lens.initializeLens()


master = Tk()
master.geometry("640x480")
focus_level = IntVar()
aperature_level = IntVar()
f = Scale(master,variable=focus_level, label="Focus", from_=1, to=10, orient=HORIZONTAL)
f.pack()

a = Scale(master,variable=aperature_level, label="Aperature", from_=1, to=10,orient=HORIZONTAL)
a.pack()

button1 = Button(master, text="Reset", width=25,command=lens.resetLens)
button2 = Button(master, text="Apply", width=25, command=lambda: lens.sync(focus_level.get(), aperature_level.get()))
button1.pack()
button2.pack()


l1 = Label(master,text=lens.name)
l1.pack()
print(lens.name)
mainloop()
#%%
print ("init lens")
for i in range(50):
    send_single_command(dev,0x0A)
    #time.sleep(0.01)

#%%

lens = LensController(dev)
lens.initializeLens()
#%%
lens.resetLens()
lens.getName()
lens.printName()
#%%
for i in range(1,11):
    level = i 
    lens.sync(level, level)
    time.sleep(1)
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
dev.Close()
