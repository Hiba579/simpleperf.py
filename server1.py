import argparse
import socket
import time


BUFFER_SIZE = 1000

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"A simpleperf server is listening on port {port}\n")
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        start_time = time.time()
        data_received = 0
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            data_received += len(data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        conn.sendall(b"ACK: BYE")
        conn.close()
        print("Transfer completed")
        print("-----------------------")
        print(f"Bytes received: {data_received}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Bandwidth: {(data_received / elapsed_time) / 10**6:.2f} MB/s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simpleperf server")
    parser.add_argument("-b", "--bind", metavar="", help="Specify IP address to bind (default: 0.0.0.0)", default="127.0.0.1")
    parser.add_argument("-p", "--port", metavar="", help="Specify port number (default: 8088)", type=int, default=8088)
    args = parser.parse_args()
    start_server(args.bind, args.port)
