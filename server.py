import socket 
import threading
import json
import time
import numpy

PORT_NO = 5002
IP = "100.86.8.123"
HOST = (IP, PORT_NO)
Clients = []
transports = []


# control the logic of the game
def send_question(data, Id):
    test_speed()

def join_game(data, Id):
    pass

def submit_answer(data, Id):
    pass

# Determine Round trip time for the client
def test_speed():
    for trans in transports:
        times = time.time()
        data = {'response': 'test'}
        data = json.dumps(data)
        trans.sendall(data.encode('utf-8'))
        data = sc.recv(1024)
        delay = (time.time() - times)/2
        print(delay)

# process the request and choose the function to run based on request pattern
def process_request(data, Id):
    for pattern in request_patterns:
            if json.loads(data.decode('utf-8'))['request'] == pattern[0]:
                pattern[1](data, Id)

request_patterns = [
    ('start', send_question),
]

class myThread (threading.Thread):
    def __init__(self, clientID_, transport_, address_):
        threading.Thread.__init__(self)
        self.clientID = clientID_
        self.address = address_
        self.transport = transport_

    def run(self):
        print(f"Start serving client {self.clientID} with address {self.address}")
        start_serving_client(self.transport, self.clientID)
        print(f"client: {self.address}, exited the game")


# This function handles the communication between client and server

def start_serving_client(trans, Id):
    while True:
        data = trans.recv(1024)
        if json.loads(data.decode('utf-8'))['data'] == 'STOP':
            data = json.loads(data.decode('utf-8'))['data']
            trans.sendall(data.encode('utf-8'))
            break
        process_request(data, Id)
            
    trans.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(HOST)
sock.listen(100)
print(f"server listening on ip {IP}, port {PORT_NO}")

clientID = 0
while True:
    sc, addr = sock.accept()
    clientID += 1
    Clients.append(addr)
    transports.append(sc)
    thread = myThread(clientID, sc, addr)
    thread.start()

