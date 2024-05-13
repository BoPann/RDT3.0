from socket import *
from time import sleep
import util

## No other imports allowed

# server port for receiver
PORT = 10101
SERVER_NAME = 'localhost'

# packet number
p_number = 1
# current seq
prev_seq = 0

# flag in used to only triggered timeout and bit error once
repeat = True



print('Receiver listening on port', PORT)
# create socket
s = socket(AF_INET, SOCK_DGRAM)
s.bind((SERVER_NAME, PORT))

# keep listening
while True:

    # receive the packet
    data, addr = s.recvfrom(2056)
    print(f"Packet num.{p_number} received: {data}")
    
    # make sleep to simulate timeout
    # flag is used so only sleep once on the same packet
    if p_number % 6 == 0 and repeat:
        # Simulate packet loss every 6 packets
        print('simulating packet loss: sleep a while to trigger timeout event on the sender side...')
        sleep(3)
        repeat = False
    
    # simulate bit errors
    # flag is used so only sleep once on the same packet
    elif not util.verify_checksum(data) or (p_number % 3 == 0 and repeat):
        print('simulating packet bit errors/corruption: ACK the previous packet!')
        response_packet = util.make_packet('', 1, prev_seq)
        s.sendto(response_packet, addr)
        repeat = False
    # simulate no error and packet is received correctly
    else:
        print(f'packet is expected, message string delivered: {data[12:].decode()}')
        print('packet is delivered, now creating and sending the ACK packet...')
        # Determine seq num from the received packet
        seq = 1 if (data[11] & 1) == 1 else 0
        # Create response packet with ACK for the current seq bum 
        response_packet = util.make_packet('', 1, seq)
        s.sendto(response_packet, addr)
        # Update previous seq num
        prev_seq = seq
        repeat = True 
    p_number += 1
    print('all done for this packet!\n')
