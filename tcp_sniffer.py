import pyshark  # http://kiminewt.github.io/pyshark/
import json
import random
from zxcvbn import zxcvbn

# change interface and src ip as needed

# TODO:
# Input for interface and ip source display filter
# link up entropy checker (zxcvbn)(remove last 16 bytes?)

def main():
    capture = pyshark.LiveCapture(interface='\Device\\NPF_{2F1DBFFB-5D87-4B88-BA83-CF0104043E2E}',display_filter='ip.src == 192.168.1.146')
    capture.sniff(timeout=10)
    print (capture)
    while True:
        try:
            p = capture.next()
        except StopIteration:
            break
        try:
            stream_data = p.data.data.binary_value
            print (stream_data)
        except AttributeError:
            pass
    results = zxcvbn(stream_data)
    print(results)
    word = results['password']
    score = results['score']
    print("word:", word)
    print("score:", score)
    if word != 4:
        print("Low string entropy: Its likely traffic is not encrypted")


main()
