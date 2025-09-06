import socket

# UDP settings
UDP_IP = "127.0.0.1"
UDP_PORT = 50000

# Manually define 11 bytes (each as int 0–255)
# Example pattern: Play all of the C's on the piano
all_Cs_message = bytearray([
    0b00001000,  # byte 0
    0b10000000,  # byte 1
    0b00000000,  # byte 2
    0b00001000,  # byte 3
    0b10000000,  # byte 4
    0b00000000,  # byte 5
    0b00001000,  # byte 6
    0b10000000,  # byte 7
    0b00000000,  # byte 8
    0b00001000,  # byte 9
    0b10000000   # byte 10
])

# Create UDP socket and send
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(all_Cs_message, (UDP_IP, UDP_PORT))

# Print message as bits for verification
print("Sent 11-byte message (bits):")
for i, b in enumerate(all_Cs_message):
    print(f"Byte {i}: {bin(b)[2:].zfill(8)}")
