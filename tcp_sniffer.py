import pyshark  # http://kiminewt.github.io/pyshark/
from zxcvbn import zxcvbn # https://github.com/dropbox/zxcvbn
import ipaddress # Standard Python Library

def main():
    flag = 1 # Set flag
    intf = input("Enter interface name to sniff on (ie eth0, enp0s3) (lo if local) from ifconfig/ipconfig:  ") # Interface input
    while flag == 1: # loop check
        filter = input("Enter IP to filter (Enter server IP to log IOTSec traffic): ") # filter Ip input
        try:
            ipaddress.ip_address(filter)  # if valid
            flag = 0  # end while loop
        except:
            print("Invalid IP")  # else repeat
    capture = pyshark.LiveCapture(interface=intf,display_filter='ip.src =='+filter, output_file="capture.pcap") # start pyshark capture with interface input and ip source input into variable capture
    capture.sniff(timeout=10) # sniff for 10 seconds
    print (capture) # print capture
    while True:
        try:
            p = capture.next() # Iterate through capture packets
        except StopIteration: # when at last packet, end
            break
        try:
            stream_data = p.data.data # Extract data from packet
            stream_data = bytes.fromhex(stream_data).decode('ascii', 'ignore') # decode hex data into ascii
            #print (stream_data)
            results = zxcvbn(stream_data) # generate string entropy using zxcvbn into varaible results
            #print(results)
            word = results['password'] # Extract word from zxcvbn
            word = word.replace('/', '//')
            score = results['score'] # Extract score from zxcvbn
            print("word:", word) # print word
            print("score:", score) # print score
            if score != 4: # If score not 4 then string likely not encrypted
                print("Low string entropy: Its likely traffic is not encrypted")
                print("\n")
            else: # If score is 4 string is likely encrypted
                print("High string entropy: Traffic is likely encrypted")
                print("\n")
        except AttributeError: # Catch attribute error
            pass

main()
