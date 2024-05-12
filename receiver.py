from socket import *
from time import sleep
import util

## No other imports allowed

PORT = 10101
SERVER_NAME = 'localhost'
SENDER_SERVER = ('localhost', 10100)

p_number = 1
while True:
    # create socket
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind((SERVER_NAME, PORT))

        print('Server listening on port', PORT)
        # machine state
        state = 0

        # keep listening
        while True:
            # receive the packet
            data, addr = s.recvfrom(2056)
            print(f"Packet num.{p_number} received: {data}")
            
            # make sleep to simulate timeout
            # flag is used so only sleep once on the same packet
            timeout_flag = True
            while p_number % 6 == 0 and timeout_flag:
                sleep(3.5)
                print("simulating packet loss: sleep a while to trigger timeout event on the sender side")
                timeout_flag = not timeout_flag
                

            # check seq number
            ack, seq = util.getAckSeq(data)
            ack = int(ack)
            seq = int(seq)
            # when seq and state not match -> have sender resend
            if seq != state:
                print("Sequence number mismatch. Resending ACK for the previous sequence number.")
                # Resend acknowledgment for the previous sequence number
                packet = util.make_packet('', (ack + 1) % 2, (seq + 1) % 2)
                s.sendto(packet, SENDER_SERVER)
                break
            
            # check checksum
            if not util.verify_checksum(data):
            # checksum not match(corrupted) -> have sender resend
                print("simulating packet bit errors/corrupted: ACK the previous packet!")
                packet = util.make_packet('', (ack + 1) % 2, (seq + 1) % 2)
                break
            print(f"packet is expected, message string delivered: {util.getMsg(data)}")
            # chcksum match, deliver data to application and send ack to sender
            print(f"packet num. {p_number} is delivered, now creating and sending the ACK packet")
            packet = util.make_packet('', ack, seq)
            s.sendto(data, addr)
            print("all done for this packet!\n\n")

            # flip the state and increase packet number
            state = (state + 1) % 2
            p_number += 1