import pyshark # http://kiminewt.github.io/pyshark/

capture = pyshark.LiveCapture(interface='loopback', display_filter='gsm_ipa') # ipa as data is sent from port 5000
capture.sniff(timeout=10)
print(capture)
packet_amount = len(capture)
packet_amount = packet_amount - 1
pkt = capture[packet_amount]
readable = pkt.tcp.payload
readable = readable.replace(':','')
readable = bytes.fromhex(readable).decode('utf-8')
print(readable)