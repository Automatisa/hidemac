#!/usr/bin/env python
# HideMAC 1.5
# Package mantained by infodox and Dark_Lightening
# www.infodox.co.cc
# blog.infodox.co.cc
# http://twitter.com/info_dox
# Credit to Trip from Hak5 for the getmac function, as mine did not work!
# This version is a more cleaned up one, with a lot fo the Python2 code ported to Python3...
# Also the ifconfig methods MAC address randomization engine has been improved!
import os
import commands
import sys
import random

# Function: Banner()
# Does fuck all, just puts out an epic banner!
def banner():
    print("  ___ ___ .__    .___          _____     _____  _________  ")
    print(" /   |   \|__| __| _/ ____    /     \   /  _  \ \_   ___ \ ")
    print("/    ~    \  |/ __ |_/ __ \  /  \ /  \ /  /_\  \/    \  \/ ")
    print("\    Y    /  / /_/ |\  ___/ /    Y    |    |    \     \____")
    print(" \___|_  /|__\____ | \___  >\____|__  |____|__  /\______  /")
    print("       \/         \/     \/         \/        \/        \/ ")
    print("")
    print("       This code is still under development. It still needs work.")
    print("Email any bugs you find in this code to infodox [at] compsoc [dot] nuigalway [dot] ie ")

# Function: amiroot()
def amiroot():
    if os.geteuid() != 0:
        print("[-] You are not root... Sudo may be of some assistance!")
        sys.exit(1)
    else:
        pass

# Function: get_ifaces() This works in 3
def get_ifaces():
        airmon = os.popen("airmon-ng")
        ifacelst = airmon.readlines()
        li=0
        for line in ifacelst:
                line = line.replace("Interface\tChipset\t\tDriver","")
                line = line.strip()
                inum = li + 1
                if line:
                        line = line.split("\t\t")
                        print (line[0])
                        ifaces = line[0]
                        return ifaces
 
# Function: randommac() as does this
def randomMAC():
    mac = [random.randint(0x00, 0xff) , 
	   random.randint(0x00, 0xff) , 
	   random.randint(0x00, 0xff) , 
	   random.randint(0x00, 0xff) , 
	   random.randint(0x00, 0xff) , 
	   random.randint(0x00, 0xff)]
    return (':'.join(map(lambda x: "%02x" % x, mac)))
    return (newmac)

# Function: getmac(iface)
def getmac(iface):
    data = commands.getoutput("ifconfig " + iface)
    words = data.split()
    found = 0
    for x in words:
        #print x
        if found != 0:
            mac = x
            break
        if x == "HWaddr":
            found = 1
    if len(mac) == 0:
        mac = 'Mac not found'
    mac = mac[:17]
    print mac

# Function: check()
def check():
    if os.path.isfile("/usr/local/bin/macchanger") == True:
        print("[*] MAC Changer is installed, using it...")
        macchanger_changemac(iface)
    else:
        print("[*] MAC Changer is not installed, using ifconfig method!")
        ifconfig_changemac(iface)

# Function: check() works
def check():
    if os.path.isfile("/usr/local/bin/macchanger") == True:
        print("MAC Changer is installed, using it...")
        macchanger_changemac(iface)
    else:
        print("MAC Changer is not installed, using ifconfig method!")
        ifconfig_changemac(iface)
 
# Function: macchanger_changemac(iface)
def macchanger_changemac(iface):
    print("[+] Changing your MAC address to something totally random...") # More statuses
    os.popen("macchanger --random " + iface) # CHANGES MAC ADDRESS!!!!!!!
 
# Function: ifconfig_changemac(iface)
def ifconfig_changemac(iface):
    print("[+] Changing your MAC address to something totally random...") # More statuses
    os.popen("ifconfig " + iface + " hw ether " + randomMAC()) 

banner()
amiroot()
print("========== Currently Available Interfaces ==========")
get_ifaces()
print("====================================================")
iface = raw_input("what interface are you changing (eg: wlan0): ") # Sets the interface to fuck with...
print("[*] Your Current MAC address is: ")
getmac(iface)
os.popen("ifconfig " + iface + " down") # Puts interface down :(
check()
os.popen("ifconfig " + iface + " up") # Puts interface back up :)
print("[*] Your New MAC address is: ")
getmac(iface)
