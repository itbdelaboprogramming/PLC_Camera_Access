import socket

def connect_to_tcp(ip, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((ip, port))
            print(f"Connected to {ip}:{port}")
            # Send the specified message
            s.sendall(b'WR MR002 1\r')
            # Receive response (optional)
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ip_address = "192.168.110.10"
    port_number = 8501
    connect_to_tcp(ip_address, port_number)