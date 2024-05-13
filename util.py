def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes
    """
   # convert everything to bytes and add them together
    checksum = 0
    # Iterate through packet in 2-byte chunks
    # this handle the odd byte as well
    for i in range(0, len(packet_wo_checksum), 2):
        # Convert 2-byte chunk to integer
        chunk = packet_wo_checksum[i:i+2]
        value = int.from_bytes(chunk, byteorder='big')
        checksum += value

    # Take one's complement and add carry
    while checksum >> 16:
        checksum = (checksum & 0xffff) + (checksum >> 16)
    checksum = ~checksum & 0xffff

    # Convert checksum to bytes
    checksum_bytes = checksum.to_bytes(2, byteorder='big')

    return checksum_bytes


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
# Extract the checksum from the packet
    packet_checksum = packet[8:10]

    # Compute the checksum of the packet excluding the checksum field
    computed_checksum = create_checksum(packet[:8] + packet[10:])

    # Compare the computed checksum with the extracted checksum
    return packet_checksum == computed_checksum

    

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # make sure your packet follows the required format!
    header = b'COMPNETW'

    # Calculate packet length, first_eight_bytes + data length
    total_length = 12 + len(data_str)
    # compute length field
    length_field = (total_length << 2) | (ack_num << 1) | seq_num
    length = length_field.to_bytes(2, "big")
    data_bytes = data_str.encode()

    # Create checksum 
    checksum = create_checksum(header + length + data_bytes)

    # construct message
    packet = header + checksum + length + data_bytes

    return packet


# extract message
def getMsg(packet):
    data = packet[12:]
    return data.decode()

###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
