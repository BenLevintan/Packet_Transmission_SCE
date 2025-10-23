class Packet:
    #initializes a packet when called
    def __init__(self, source_address, destination_address, sequence_number,
                 is_ack=False, data=None):
        self.__source_adress=source_address
        self.__destination_adress=destination_address
        self.__sequence_number=sequence_number
        self.__is_ack=is_ack
        self.__data=data
        
    #prints out the current packet's information
    def __repr__(self):
        return f"Packet(Source IP:{self.get_source_address()}, Dest IP: {self.get_destination_address()},#Seq: {self.get_sequence_number()}, Is ACK: {self.get_is_ack()}, Data: {self.get_data()}"
    #returns the current source IP address  
    def get_source_address(self):
        return self.__source_adress
    #returns the current destination IP address        
    def get_destination_address(self): 
        return self.__destination_adress
        
    # returns thecurrent sequence number
    def get_sequence_number(self):
        return self.__sequence_number
        
    #sets the current sequence number to the one given
    def set_sequence_number(self, seq_num):
        self.__sequence_number=seq_num
        
    #  returns the current is_ack value
    def get_is_ack(self):
        return self.__is_ack
        
    # returns the current data
    def get_data(self):
        return self.__data
        

class Communicator:
    #initializes a communicator when called
    def __init__(self, address):
        self.__address=address
        self.__current_seq_num=None

    #returns the current IP address
    def get_address(self):
        return self.__address
        
    #returns the current sequence number
    def get_current_sequence_number(self):
        return self.__current_seq_num
        
    #sets the current sequence number to one given
    def set_current_sequence_number(self, seq_num):
        self.__current_seq_num=seq_num
         
    #sends a packet
    def send_packet(self, packet):
        print(f"Sender: Packet Seq Num: {packet.get_sequence_number()} was sent")
        return packet 
    #changes the current sequence number by one
    def increment_current_seq_num(self):
        if self.__current_seq_num is not None:
            self.__current_seq_num += 1

class Sender(Communicator):
    #initializes a sender when called
    def __init__(self, address, num_letters_in_packet):
        super().__init__(address)
        self.__num_letters_in_packet=num_letters_in_packet
    #returns the current number of letters in a packet
    def prepare_packets(self, message, destination_address):

        if not message:                                         # empty string is equivalent false
            raise ValueError("Message cannot be empty")         # throw exeption if massage is empty
           
        contains_valid_char = False                             # flag goes up if there is a valid char
        for char in message:                                    # go throw the chars is the string
            if ((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')  or char == ' '):
                contains_valid_char = True                      # if it contains a valid char, raise the flag and go out the loop
                break 
            if not contains_valid_char:                                 # if the flag is down, just throw an error
                raise ValueError("Message contains only invalid characters")
            
        packetlist=[]
        for i in range(0,len(message),num_letters_in_packet):#checks the packet and returns a list of packets
            packet_data=message[i:i+num_letters_in_packet]
            packet=Packet(self.get_address(),destination_address,i//num_letters_in_packet,data=packet_data)
            packetlist.append(packet)
        return packetlist

    #checks if the acknowledgment packet is true and returns a boolean value
    def receive_ack(self, acknowledgment_packet):
        return Packet.get_is_ack(acknowledgment_packet)


class Receiver(Communicator):
    #initializes a receiver when called
    def __init__(self, address):
        self.received_packets=[]
        super().__init__(address)

    #checks if the packet is in the list of received packets and gives the packet to the receiver
    def receive_packet(self, packet):
        self.received_packets.append(packet)
        Acknowledgment=Packet(packet.get_destination_address(),packet.get_source_address(),packet.get_sequence_number(),is_ack=True)
        print(f"Receiver: Received packet seq num:{packet.get_sequence_number()}")
        return Acknowledgment
    
    #constructs a readable message from the received packet's data
    def get_message_by_received_packets(self):
        constructmessage=""
        for packet in self.received_packets:
            constructmessage+=packet.get_data()
        return constructmessage


if __name__ == '__main__':
    source_address = "192.168.1.1"
    destination_address = "192.168.2.2"
    message = "What is up?"
    num_letters_in_packet = 3

    sender = Sender(source_address, num_letters_in_packet)
    receiver = Receiver(destination_address)

    packets = sender.prepare_packets(message, receiver.get_address())

    # setting current packet
    start_interval_index = packets[0].get_sequence_number()
    # setting current packet in the sender and receiver
    sender.set_current_sequence_number(start_interval_index)
    receiver.set_current_sequence_number(start_interval_index)

    # setting the last packet
    last_packet_sequence_num = packets[-1].get_sequence_number()
    receiver_current_packet = receiver.get_current_sequence_number()

    while receiver_current_packet <= last_packet_sequence_num:
        current_index = sender.get_current_sequence_number()
        packet = packets[current_index]
        packet = sender.send_packet(packet)

        ack = receiver.receive_packet(packet)

        result = sender.receive_ack(ack)

        if result == True:

            sender.increment_current_seq_num()
            receiver.increment_current_seq_num()

        receiver_current_packet = receiver.get_current_sequence_number()

    full_message = receiver.get_message_by_received_packets()
    print(f"Receiver message: {full_message}")