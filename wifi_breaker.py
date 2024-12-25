import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import time

# Function to run system commands
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(), result.stderr.decode()

# Function to switch Wi-Fi adapter to monitor mode
def set_monitor_mode(interface):
    # Check if the interface is already in monitor mode
    output, error = run_command(f"iw dev {interface} info")
    if "mode monitor" in output:
        return f"{interface} is already in monitor mode."
    
    run_command(f"sudo ip link set {interface} down")
    run_command(f"sudo ip link set {interface} name {interface}mon")
    run_command(f"sudo ip link set {interface}mon up")
    return f"{interface} is now in monitor mode."

# Function to switch Wi-Fi adapter back to managed mode
def set_managed_mode(interface):
    # Check if the interface is already in managed mode
    output, error = run_command(f"iw dev {interface} info")
    if "mode managed" in output:
        return f"{interface} is already in managed mode."
    
    run_command(f"sudo ip link set {interface}mon down")
    run_command(f"sudo ip link set {interface} name {interface}")
    run_command(f"sudo ip link set {interface} up")
    return f"{interface} is now in managed mode."

# Function to scan for available networks and return the list of MAC addresses (BSSIDs)
def scan_networks(interface):
    # Run airodump-ng for a more extended period to capture networks
    output, error = run_command(f"sudo airodump-ng --output-format csv --write temp_scan {interface}mon")
    
    if error:
        print(f"Error scanning networks: {error}")
        return []
    
    # Wait for a few seconds to ensure airodump-ng has time to capture networks
    time.sleep(5)
    
    # Parse the output CSV file to extract BSSIDs
    networks = []
    with open("temp_scan-01.csv", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Station MAC"):
                continue  # Skip header lines
            fields = line.split(",")
            if len(fields) > 0:
                networks.append(fields[0])  # The first field is the BSSID
    return networks

# Function to handle Wi-Fi scan button click
def handle_scan_button(interface):
    bssids = scan_networks(interface)
    if bssids:
        listbox.delete(0, tk.END)  # Clear current listbox
        for bssid in bssids:
            listbox.insert(tk.END, bssid)
    else:
        messagebox.showerror("Scan Error", "Failed to scan networks or no networks found.")

# Function to handle mode switching
def handle_mode_switch(interface, mode):
    try:
        if mode == "Monitor":
            status = set_monitor_mode(interface)
            mode_label.config(text=f"Mode: Monitor ({interface}mon)")
        else:
            status = set_managed_mode(interface)
            mode_label.config(text=f"Mode: Managed ({interface})")
        messagebox.showinfo("Mode Switch", status)
    except Exception as e:
        messagebox.showerror("Mode Switch Error", f"Error switching modes: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Wi-Fi Network Scanner and Mode Switcher")

# Labels and Buttons
interface_label = tk.Label(root, text="Enter Wi-Fi Interface (e.g., wlan0):")
interface_label.pack(pady=5)

interface_entry = tk.Entry(root)
interface_entry.pack(pady=5)

mode_label = tk.Label(root, text="Mode: Managed")
mode_label.pack(pady=5)

scan_button = tk.Button(root, text="Scan for Networks", command=lambda: handle_scan_button(interface_entry.get()))
scan_button.pack(pady=5)

mode_switch_button = tk.Button(root, text="Switch to Monitor Mode", 
                               command=lambda: handle_mode_switch(interface_entry.get(), "Monitor"))
mode_switch_button.pack(pady=5)

switch_to_managed_button = tk.Button(root, text="Switch to Managed Mode", 
                                     command=lambda: handle_mode_switch(interface_entry.get(), "Managed"))
switch_to_managed_button.pack(pady=5)

# Listbox to display available networks
listbox = tk.Listbox(root, width=40, height=10)
listbox.pack(pady=5)

# Start the GUI loop
root.mainloop()

