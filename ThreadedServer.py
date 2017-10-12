import sys
import socket
import json
import threading
import collections
import time
import unittest

# from Tkinter import *

# TCP_IP = '192.168.1.100'
TCP_IP = ''
TCP_PORT = 2000
BUFFER_SIZE = 1024

allClients = set()
allClients_lock = threading.Lock()

states = {'stop': 0, 'forward': 1, 'left': 2, 'right': 3, 'back': 4}
currentState = states.get('forward')

class ThreadedServer(unittest.TestCase):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print ("Started listening for connections...")
        self.sock.listen(5) # allow a maximum of 5 connections.
        while True:
            client, address = self.sock.accept()
            # client.settimeout(500)
            sthread = threading.Thread(target = self.listenToClient,args = (client, address)).start()
            '''sthread.start()
            print("start")
            time.sleep(0.000001)
            fake_client = socket.socket()
            fake_client.settimeout(10)
            fake_client.connect(('192.168.1.100', 2000))
            fake_client.close()
            print("end")
            sthread.join()'''
                        
    def listenToClient(self, client, address):
        print ("Accepted connection from:", address)
        with allClients_lock:
            allClients.add(client)

        while True:
            with allClients_lock:
                    print ("Start Json data sent to client!")
                    client.send(b'{')
                    client.send(b'"')
                    client.send(b'd')
                    client.send(b'i')
                    client.send(b'r')
                    client.send(b'"')
                    client.send(b':')
                    client.send(b'5')
                    client.send(b'}')
                    print ("End Json data sent to client1!")
                    time.sleep(1);
                    data = client.recv(BUFFER_SIZE)
                    print (data)
                    print (self.assertTrue(data, '{"dir":stop}'))
                    print ("Start Json data sent to client!")
                    client.send(b'{')
                    client.send(b'"')
                    client.send(b'd')
                    client.send(b'i')
                    client.send(b'r')
                    client.send(b'"')
                    client.send(b':')
                    client.send(b'2')
                    client.send(b'}')
                    print ("End Json data sent to client2!")
                    time.sleep(1);
                    data = client.recv(BUFFER_SIZE)
                    print (data)
                    print ("Start Json data sent to client!")
                    client.send(b'{')
                    client.send(b'"')
                    client.send(b'd')
                    client.send(b'i')
                    client.send(b'r')
                    client.send(b'"')
                    client.send(b':')
                    client.send(b'3')
                    client.send(b'}')
                    print ("End Json data sent to client3!")
                    time.sleep(1);
                    data = client.recv(BUFFER_SIZE)
                    print (data)
                    print ("Start Json data sent to client!")
                    client.send(b'{')
                    client.send(b'"')
                    client.send(b'd')
                    client.send(b'i')
                    client.send(b'r')
                    client.send(b'"')
                    client.send(b':')
                    client.send(b'4')
                    client.send(b'}')
                    print ("End Json data sent to client4!")
                    time.sleep(4);
                    data = client.recv(BUFFER_SIZE)
                    print (data)
                    print ("Start Json data sent to client!")
                    client.send(b'{')
                    client.send(b'"')
                    client.send(b'd')
                    client.send(b'i')
                    client.send(b'r')
                    client.send(b'"')
                    client.send(b':')
                    client.send(b'5')
                    client.send(b'}')
                    print ("End Json data sent to client5!")
                    time.sleep(1);
                    data = client.recv(BUFFER_SIZE)
                    print (data)
                    if data:
                        '''
                        # Set the response to echo back the received data. 
                        charSent = data
                        with allClients_lock:
                            # responseLoaded = json.loads(response)
                            print ('Data: %s received from %s'% (charSent, client.getsockname()))
                        '''

                        '''
                            if str(responseLoaded['dir']) == "Initial Handshake":
                                print ('Initial Handshake was successful! Enabling rover movement!')
                                responseLoaded = {};
                                responseLoaded['dir'] = 0;
                            elif responseLoaded['dir'] == 0:
                                responseLoaded['dir'] = 1;
                            elif responseLoaded['dir'] == 1:
                                responseLoaded['dir'] = 2;
                            elif responseLoaded['dir'] == 2:
                                responseLoaded['dir'] = 3;
                            elif responseLoaded['dir'] == 3:
                                responseLoaded['dir'] = 4;
                            elif responseLoaded['dir'] == 4:
                                responseLoaded['dir'] = 0; #states got changed, check numbers

                            responseToSend = json.dumps(responseLoaded)
                        '''                 



if __name__ == "__main__":

    '''
    root = Tk()
    root.title("Server")
    root.geometry("150x80")
    app = Frame(root)
    app.grid()
    '''

    '''
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle("ECE 4534 Team 5 Server")

    # Create a button in the window
    btn = QPushButton("OK", widget)

    # Create the actions
    @pyqtSlot()
    def on_click():
        print('clicked')

    @pyqtSlot()
    def on_press():
        print('pressed')

    @pyqtSlot()
    def on_release():
        print('released')
     
    # connect the signals to the slots
    btn.clicked.connect(on_click)
    btn.pressed.connect(on_press)
    btn.released.connect(on_release)
    widget.show()
    app.exec_()
    '''

    myServer = ThreadedServer(TCP_IP, TCP_PORT)

    while True:
        # root.mainloop()
        myServer.listen()
