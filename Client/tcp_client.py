import socket
import time


def get_user_input():
    # while True:
    c_input = input("""
You may ask a question of the following:
    1. What will be the highest value of Nvidia stock on [YYYYMMDD] if the open value is [Number]?
    2. Date: [YYYYMMDD], Open: [Number]
    3. [YYYYMMDD] [Number]

    e.g. Date: 20150920, Open: 130
    
    Your input: """)

    return c_input


def confirm_continue():
    while True:
        c_input = input("""
    Would you like to continue? (Y/N)
    """)
        if c_input.strip().upper() == "Y":
            return True
        elif c_input.strip().upper() == "N":
            return False


def create_connection():
    HOST = "127.0.0.1"
    PORT = 65432

    print(f"Attempting to connect to {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        user_input = get_user_input().encode("utf-8")

        s.sendall(user_input)
        data = s.recv(1024).decode("utf-8")
        print("\nReceived", repr(data))

        resume = confirm_continue()
        if not resume:
            s.close()
            break


if __name__ == "__main__":
    connected = False
    for i in range(10):
        if not connected:
            try:
                create_connection()
                connected = True
            except ConnectionRefusedError:
                time.sleep(1)
                print("Server refused connection. Reattempting...")
