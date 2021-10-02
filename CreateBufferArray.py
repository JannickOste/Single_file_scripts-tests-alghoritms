binarySet = bytearray()
# Creating a bytearray
for i in ["hello", "you", "smello"]:
    binaryData = bytes(str.encode(i)) # Encode data.
    # Add Size (in structure of 4 bytes) + data to the set.
    binarySet += int(len(binaryData)).to_bytes(4, "big")
    binarySet += binaryData


i = 0
while True:
    set_size = int.from_bytes(binarySet[i:i+4], "big") # Fetch size of current set slice.
    if set_size == 0:
        break
    i += 4 # Skip the set size (4bytes)
    # Wala here is your slice:
    print(binarySet[i:i+set_size])
    i += set_size

