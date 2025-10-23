# Packet Transmission Protocol Project

## 📘 Overview
This project implements a **simulation of a simple packet transmission protocol**, inspired by the transport layer model studied in a computer networks course.  
The goal is to simulate the process of sending a message from a **sender** to a **receiver** using **packets**, handling acknowledgments (ACKs), and reconstructing the message on the receiving side.

The implementation follows the assignment specifications provided in  
**"פרויקט תקשורת מחשבים תשפ״ד 2024"**.

---

## 🧩 Project Structure
### File: `PacketTransmissionProtocolProject.py`

This file contains all the classes and logic for the packet transmission simulation.

### Main Components

#### 1. `Packet`
Represents a data packet being transmitted between the sender and receiver.

**Attributes:**
- `source_address` – IP address of the sender.
- `destination_address` – IP address of the receiver.
- `sequence_number` – The packet's position in the message sequence.
- `is_ack` – Boolean flag indicating whether the packet is an acknowledgment (ACK).
- `data` – The data (portion of the message) stored in the packet.

**Key Methods:**
- `__repr__()` — Returns a human-readable description of the packet.
- `get_source_address()`, `get_destination_address()`, `get_sequence_number()`, `get_is_ack()`, `get_data()` — Getter methods.
- `set_sequence_number(seq_num)` — Setter for the sequence number.

---

#### 2. `Communicator`
An abstract class representing a communication entity (both sender and receiver inherit from this).

**Attributes:**
- `address` — The entity’s IP address.
- `current_seq_num` — The current sequence number being processed.

**Key Methods:**
- `get_address()`, `get_current_sequence_number()`, `set_current_sequence_number(seq_num)`
- `send_packet(packet)` — Prints and returns the sent packet.
- `increment_current_seq_num()` — Increases the current sequence number by one.

---

#### 3. `Sender` (inherits from `Communicator`)
Represents the **sending entity** that divides a message into packets and transmits them.

**Attributes:**
- `num_letters_in_packet` — Defines how many characters are stored in each packet.

**Key Methods:**
- `prepare_packets(message, destination_address)`  
  Splits the message into smaller packets, validates input, and returns a list of `Packet` objects.
- `receive_ack(acknowledgment_packet)`  
  Checks whether a received packet is an acknowledgment (ACK).

**Example of packet division:**  
Message: `"What is up?"` with `num_letters_in_packet = 3`  
→ Packets: `["Wha", "t i", "s u", "p? "]`

---

#### 4. `Receiver` (inherits from `Communicator`)
Represents the **receiving entity** that accepts packets and reconstructs the message.

**Attributes:**
- `received_packets` — A list storing all received packets.

**Key Methods:**
- `receive_packet(packet)`  
  Receives a packet, stores it, prints a message, and returns an acknowledgment packet (ACK).
- `get_message_by_received_packets()`  
  Concatenates the data from all received packets into the full original message.

---

## ⚙️ Main Program Flow
When the program is run directly (`if __name__ == "__main__":`):
1. The sender and receiver are initialized with their IP addresses.
2. The sender splits the input message into packets using `prepare_packets()`.
3. Each packet is sent in sequence:
   - The sender sends a packet.
   - The receiver receives it and responds with an ACK.
   - The sender checks the ACK and continues with the next packet.
4. Once all packets are sent and acknowledged, the receiver reconstructs and prints the full message.

**Example Output:**
Sender: Packet Seq Num: 0 was sent
Receiver: Received packet seq num: 0
Sender: Packet Seq Num: 1 was sent
Receiver: Received packet seq num: 1
...
Receiver message: What is up?

markdown
Copy code

---

## 🧠 Error Handling
- **Empty message:** Raises `ValueError("Message cannot be empty")`
- **Invalid message characters:** Raises `ValueError("Message contains only invalid characters")`

Valid characters include:
- English letters (`A–Z`, `a–z`)
- Spaces (`' '`)
