import socket
import threading
from _thread import *
import re
import machine_learning as ml

print_lock = threading.Lock()
trained_model = ml.model_training()


def check_date_format(value):
    pattern = r'^(\d{4})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$'
    match = re.match(pattern, value)

    try:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)

        return year, month, day
    except (IndexError, ValueError, AttributeError):
        raise ValueError("regex pattern failed to find value")


def get_values(text):
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    return numbers[:2]


def threaded_server(c):
    while True:
        data = c.recv(1024)
        if not data:
            print("Connection closed")
            print_lock.release()
            break
        text = str(data.decode("utf-8"))
        print(f"\nReceived data: {text}")
        values = get_values(text)
        try:
            date_check = check_date_format(values[0])
            year, month, day = date_check
        except (IndexError, ValueError):
            print("Error: Invalid date provided.")
            reply = "Please enter a valid date."
            c.send(reply.encode("utf-8"))
            continue
        try:
            open_value = values[1]
        except IndexError:
            print("Error: Invalid opening value provided.")
            reply = "Please enter a valid opening value"
            c.send(reply.encode("utf-8"))
            continue

        print(f"Evaluating {year}/{month}/{day} | {open_value}")
        result = ml.evaluate_model(trained_model, int(year), int(month), int(day), float(open_value))
        try:
            result_value = result[0][0]
        except IndexError:
            print("Error: AI Model failed to produce result")
            reply = "Due to unforeseen error, the AI has failed to evaluate the high value..."
            c.send(reply.encode("utf-8"))
            continue
        reply = f"Your estimated high value for an open value of {open_value} on {year}/{month}/{day} is {result_value}"
        c.send(reply.encode("utf-8"))
    c.close()


def create_listen_socket():
    HOST = "127.0.0.1"
    PORT = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(4)
    print("\nSocket is listening")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print(f"Connected to : {addr[0]}:{addr[1]}")
        start_new_thread(threaded_server, (c,))


if __name__ == "__main__":
    create_listen_socket()
