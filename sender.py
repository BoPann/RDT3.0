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
        self.SENDER_SERVER = ('localhost', 10190)
        self.seq_num = 0
        self.p_number = 0
        self.first_transmission = True

  def rdt_send(self, app_msg_str):
      """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
      # make packet
      # the packet will have ack 0 because the first packet is not a ack packet
      pkt = util.make_packet(app_msg_str, 0, self.seq_num)
      if self.first_transmission:
          # print the packet content only in first transmission
          print("original message string:", app_msg_str)
          print("packet created:", pkt)
          
      
      # create socket
      with socket(AF_INET, SOCK_DGRAM) as s:
          s.settimeout(3)

          # send packet to receiver
          s.sendto(pkt, self.RECEIVER_SERVER)
          self.p_number += 1
          print(f"packet num.{self.p_number} is successfully sent to the receiver.")

          try:
              # receive the ack packet
              ack_packet, addr = s.recvfrom(2048)
              # ack, seq = util.getAckSeq(ack_packet)
              # ack = int(ack)

              ack = 1 if (ack_packet[11] & 1) == 1 else 0

              # when get the right ack number
              if ack == self.seq_num:
                  print(f"packet is received correctly: seq. num {self.seq_num} = ACK. num {ack} all done!\n")
                  self.seq_num = 0 if self.seq_num == 1 else 1 
                  self.first_transmission = True

              # did not get the correct ack number
              else:
                  # s.sendto(pkt, self.RECEIVER_SERVER)
                  print("receiver acked the previous pkt, resend!\n")
                  print('[ACK-Previous retransmission]: ' + app_msg_str)
                  self.first_transmission = False
                  self.rdt_send(app_msg_str)
              s.close()
                  
          except timeout:
              print("socket timeout! Resend!\n")
              print('[timeout retransmission]: ' + app_msg_str)
              # s.sendto(pkt, self.RECEIVER_SERVER)
              self.first_transmission = False
              self.rdt_send(app_msg_str)



  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   