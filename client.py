import socket 
import threading
import json
import time

PORT_NO = 5002
HOST = ("100.86.8.123", PORT_NO)

exitFlag = False

def test(data, sc):
    sc.sendall(data)

def question(data):
    pass
def feedback(data):
    pass
# process the request and choose the function to run based on request pattern

response_patterns = [
    ('test', test),
]


def process_request(data, sc):
    for pattern in response_patterns:
            if json.loads(data.decode('utf-8'))['response'] == pattern[0]:
                return pattern[1](data, sc)
    print('Not a valid request')


def RecvDataHandler(sc):
    while True:
        data = sc.recv(1024)
        print(data.decode('utf-8'))
        if data.decode('utf-8') == 'STOP':
            print(1)
            exitFlag = True
            break
        process_request(data, sc)

def SendDataHandler(sc):
    # while not exitFlag:
    #     # req = input('request: ')
    #     # data = input('data: ') 
    time.sleep(1)
    data = (json.dumps({'request':'start', 'data':''})).encode('utf-8')
    sc.sendall(data)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)
print('connected to the server')

RecvThread = threading.Thread(target=RecvDataHandler, args=(sock,))
SendThread = threading.Thread(target=SendDataHandler, args=(sock,))

RecvThread.start()
SendThread.start()

RecvThread.join()
SendThread.join()

sock.close()