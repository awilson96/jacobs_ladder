import socket

# UDP settings
UDP_IP = "127.0.0.1"
UDP_PORT = 50000

# Helper function to make header exactly 25 chars
def make_header(name):
    name = name[:25]  # truncate if longer
    return name.ljust(25).encode('ascii')  # pad with spaces to 25 bytes

# Example 11-byte mask: play all C's on the piano
all_Cs_mask = bytearray([
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

all_off_mask = bytearray([0]*11)

# Construct the UDP message
message = bytearray()
# Block 1: Live keys
message += make_header("Live keys")
message += all_Cs_mask
# Block 2: C Major suggestion
message += make_header("C Major")
message += all_Cs_mask
# Block 3: A Major suggestion
message += make_header("A Major")
message += all_Cs_mask
# Block 4: B Major suggestion
message += make_header("B Major")
message += all_Cs_mask
# Block 5: D Major suggestion
message += make_header("D Major")
message += all_Cs_mask

# Send via UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (UDP_IP, UDP_PORT))

# Verification output
print("Sent UDP message with 2 blocks:")
offset = 0
block_size = 25 + 11  # header + mask

while offset < len(message):
    header = message[offset:offset+25].decode('ascii').strip()
    mask = message[offset+25:offset+36]  # 11 bytes
    print(f"Header: {header}")
    print("Mask bits:")
    for i, b in enumerate(mask):
        print(f" Byte {i}: {bin(b)[2:].zfill(8)}")
    offset += block_size
    print("-" * 40)
