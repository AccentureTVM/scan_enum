#!/usr/bin/env python
import subprocess
import sys

def main(args):
    if len(args) != 2:
        print("Usage: snmprecon.py <ip address>")
        return

    snmpdetect = 0
    ip_address = args[1]

    ONESIXONESCAN = "onesixtyone %s" % (ip_address)
    results = subprocess.check_output(ONESIXONESCAN, shell=True).strip()

    if results != "":
        if "Windows" in results:
            results = results.split("Software: ")[1]
            snmpdetect = 1
        elif "Linux" in results:
            results = results.split("[public] ")[1]
            snmpdetect = 1
        if snmpdetect == 1:
            print("[*] SNMP running on " + ip_address + "; OS Detect: " + results)
            SNMPWALK = "snmpwalk -c public -v1 %s 1 > discovery/snmp/%s_snmpwalk.txt" % (ip_address, ip_address)
            results = subprocess.check_output(SNMPWALK, shell=True)

    NMAPSCAN = "nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes %s" % (ip_address)
    results = subprocess.check_output(NMAPSCAN, shell=True)
    resultsfile = "discovery/snmp/" + ip_address + "_snmprecon.txt"
    f = open(resultsfile, "w")
    f.write(results)
    f.close

if __name__=='__main__':
    main(sys.argv)
