from socket import *
import util

class Sender:
  def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.RECEIVER_SERVER = ('localhost', 10101)
        self.SENDER_SERVER = ('localhost', 10100)
        self.ack_num = 0
        self.seq_num = 0
        self.p_number = 1

  def rdt_send(self, app_msg_str):
      """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
      

      while True:
        # create socket
        with socket(AF_INET, SOCK_DGRAM) as s:
            
            # make packet
            print("original message string:", app_msg_str)
            pkt = util.make_packet(app_msg_str, self.ack_num, self.seq_num)
            print("packet created:", pkt)

            # send packet to receiver
            s.bind(self.SENDER_SERVER)
            s.sendto(pkt, self.RECEIVER_SERVER)
            while True:
              try:
                  s.settimeout(2)
                  ack_packet, addr = s.recvfrom(2048)
                  # print('Received a message from', addr, ':', ack_packet)
                  print(f"packet num.{self.p_number} is successfully sent to the receiver.")
                  ack, seq = util.getAckSeq(ack_packet)
                  ack = int(ack)
                  seq = int(seq)
                  # print("seq: ", seq)
                  # print("my seq: ", self.seq_num)
                  # print("ack received: ", ack)
                  # print("my ack: ", self.ack_num)

                  # when get the right ack number
                  if ack == self.ack_num:
                      break
                  # did not get the correct ack number
                  else:
                      s.sendto(pkt, self.RECEIVER_SERVER)
                      print("receiver acked the previous pkt, resend!")
                      
              except timeout:
                  s.sendto(pkt, self.RECEIVER_SERVER)
                  print("socket timeout! Resend!\n\n")

        print(f"packet is received correctly: seq. num {self.seq_num} = ACK. num {self.ack_num} all done!\n\n")
        self.seq_num = (self.seq_num + 1) % 2
        self.ack_num = (self.ack_num + 1) % 2
        self.p_number += 1
        break

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   