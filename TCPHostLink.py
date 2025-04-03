import socket

class KeyenceTCPClient:
    def __init__(self, ip, port):
        """
        Initialize the Keyence TCP/IP client with the given IP address and port.
        """
        self.ip = ip
        self.port = port

    def send_command(self, command):
        """
        Send a command to the Keyence device and receive the response.

        Args:
            command (str): The command to send to the Keyence device.

        Returns:
            str: The response from the Keyence device.
        """
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to the server
                s.connect((self.ip, self.port))
                print(f"Connected to {self.ip}:{self.port}")
                
                # Send the specified command
                s.sendall(command.encode() + b'\r')
                
                # Receive response
                response = s.recv(1024)
                return response.decode()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None