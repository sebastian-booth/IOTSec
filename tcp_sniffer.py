#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyshark  # http://kiminewt.github.io/pyshark/
import json
import random
from zxcvbn import zxcvbn

# change interface and src ip as needed

def main():
    capture = \
        pyshark.LiveCapture(interface='\Device\\NPF_{2F1DBFFB-5D87-4B88-BA83-CF0104043E2E}'
                            ,
                            display_filter='ip.src == 192.168.1.146'
                            )

                               # ipa as data is sent from port 5000

    capture.sniff(timeout=10)
    print (capture)
    while True:
        try:
            p = capture.next()
        except StopIteration:
            break
        try:
            print (p.data.data.binary_value)
        except AttributeError:
            pass


main()
