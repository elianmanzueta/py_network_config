import tkinter as tk
from netmiko import ConnectHandler
import sys
import re

# Redirector writes terminal output into txt_progress 
def redirector(inputStr):
    txt_progress.insert(tk.INSERT, inputStr)

sys.stdout.write = redirector 

cisco = {
    'device_type':'cisco_ios',
    'host':'10.10.20.172',
    'username':'elian',
    'password':'cisco123',
    'secret':'cisco'
}

port_modes = [
    'trunk',
    'access'
]

try:
    net_connect = ConnectHandler(**cisco)
except:
    print("Cannot connect!")
else:
    pass 

show_interfaces = net_connect.send_command("show ip int br")
options = list(re.findall('Fast|Gigabit\w+/\w', show_interfaces)) # Grab interfaces

# Grabs interface from interface_menu
def getInterface(selection):
    global interface
    interface = selection 
    print(f"Selected interface {interface}")

# Grabs VLAN from ent_vlan 
def getVLAN():
    global vlan
    vlan = (ent_vlan.get())
    if port_mode == 'access':
        print(f"Seleted VLAN {vlan}")
    elif port_mode == 'trunk':
        print(f"Selected VLANs {vlan}")
        vlan = ', '.join(vlan.split(" "))
def getPortMode(selection):
    global port_mode
    port_mode = selection
    print(f"Selected port mode {port_mode}")
# Executes command 
def assignVLAN():
    # send_config_set in netmiko 
    net_connect.enable() 
    output = net_connect.send_config_set([f'interface {interface}', f'switchport mode {port_mode}', f'switchport access vlan {vlan}', 'exit'])
    print(output)
    complete = "Complete"
    complete_txt = complete.center(80, "=")
    print(complete_txt)
    output = net_connect.send_command('show vlan') # Show changes
    print(output)


# TKINTER
window = tk.Tk()
window.title("VLAN Assignment")

# Interface Selection
interface_selection = tk.StringVar(window) 
interface_selection.set("Select your desired interface") 
trunk_selection = tk.StringVar(window)
trunk_selection.set("Select your port mode")
frm_interface = tk.Frame(master=window) 
frm_interface.pack() 
interface_menu = tk.OptionMenu(frm_interface, interface_selection, *options, command=getInterface) # Interface
interface_menu.grid(column=0, row=0) 
trunk_menu = tk.OptionMenu(frm_interface, trunk_selection, *port_modes, command=getPortMode) # Port mode
trunk_menu.grid(column=1, row=0)

# VLAN Assignment 
frm_vlan =tk.Frame(master=window, borderwidth=3)
frm_vlan.pack() 
lbl_beginning = tk.Label(master=frm_vlan, text="Choose your VLAN(s)")
lbl_beginning.grid(column=0, row=1) 
ent_vlan = tk.Entry(master=frm_vlan, text="VLAN", width=30)
ent_vlan.grid(column=1, row=1,  sticky='w')
btn_submit = tk.Button(master=frm_vlan, text="Confirm", command=getVLAN) # Get VLAN
btn_submit.grid(column=1, row=1, sticky='e')

# Execute commands 
btn_compile = tk.Button(text="Assign VLAN", command=assignVLAN) 
btn_compile.pack() 

# Progress
txt_progress = tk.Text()
txt_progress.pack() 

# Start
window.mainloop() 