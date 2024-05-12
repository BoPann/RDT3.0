from socket import *
from time import sleep
import util

## No other imports allowed

PORT = 10101
SERVER_NAME = 'localhost'

p_number = 0
# machine state
prev_seq = 0



print('Receiver listening on port', PORT)
# create socket
s = socket(AF_INET, SOCK_DGRAM)
s.bind((SERVER_NAME, PORT))

# keep listening
while True:

    # receive the packet
    data, addr = s.recvfrom(2056)
    print(f"Packet num.{p_number} received: {data}")
    p_number += 1
    
    # make sleep to simulate timeout
    # flag is used so only sleep once on the same packet
    if p_number % 6 == 0:
        # Simulate packet loss every 6 packets
        print('simulating packet loss: sleep a while to trigger timeout event on the sender side...')
        sleep(10)

    elif not util.verify_checksum(data) or p_number % 3 == 0:
        print('simulating packet bit errors/corruption: ACK the previous packet!')
        response_packet = util.make_packet('', 1, prev_seq)
        s.sendto(response_packet, addr)
    else:
        print(f'packet is expected, message string delivered: {util.getMsg(data)}')
        print('packet is delivered, now creating and sending the ACK packet...')
        # Determine seq num from the received packet
        seq = 1 if (data[11] & 1) == 1 else 0
        # Create response packet with ACK for the current seq bum 
        response_packet = util.make_packet('', 1, prev_seq)
        s.sendto(response_packet, addr)
        # Update previous seq num
        previous_seq = seq
        
    print('all done for this packet!\n')
