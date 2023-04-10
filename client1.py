import argparse
import socket
import time


def send_data(s, data_size, time_duration):
    # Generate data to send
    data = bytearray(data_size)
    data[0] = 1

    # Send data in chunks of 1000 bytes
    chunk_size = 1000
    num_chunks = data_size // chunk_size
    start_time = time.time()

    for i in range(num_chunks):
        s.sendall(data[i * chunk_size:(i + 1) * chunk_size])
        time.sleep(0.001)  # Add a small delay to avoid overwhelming the server

    # Send the last chunk (if any)
    if data_size % chunk_size != 0:
        s.sendall(data[num_chunks * chunk_size:])

    # Send "BYE" message to indicate end of transfer
    s.sendall(b"BYE")

    # Wait for acknowledgement
    ack = s.recv(1024)
    if ack == b"ACK: BYE":
        end_time = time.time()
        elapsed_time = end_time - start_time
        bandwidth = (data_size / elapsed_time) / 1000000  # in MB/s
        print(f"Transfer complete. Data size: {data_size} bytes, Time taken: {elapsed_time:.3f} s, Bandwidth: {bandwidth:.3f} MB/s")
    else:
        print("Error: Did not receive acknowledgement from server.")

    # Close the socket
    s.close()

def run_client(server_address, server_port, data_size, time_duration):
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server = (server_address, server_port)
    s.connect(server)

    # Send data and measure bandwidth
    send_data
