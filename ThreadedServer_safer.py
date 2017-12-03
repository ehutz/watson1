import sys
import socket
import json
import threading
import time
import datetime

TCP_IP = '' # listen to all IPs on the network.
TCP_PORT = 2000 # listen on port 2000.
BUFFER_SIZE = 1024 # maximum number of bytes of data that can be sent and received through the socket's buffer.
BACKLOG = 2 # allow a maximum of 2 connections.
TIMEOUT = 10000 # 5 second timeout on the socket.

NEED_TO_RECONNECT = False

allClients = set()
allClients_lock = threading.Lock()

'''
Define a set of game states that the server can be in.
In the listenToClient loop, check the state, and send the appropriate messages.
If a client were to disconnect, send the current status of the game to the client once it reconnects.
'''

class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    # When one rover suddenly disconnects, we want to make the other rover stop until the other rover reconnects and gets the updated game info.
    def makeOtherRoverPause(self, allClients):
        print ("Making other client pause!")
        print ("There are " + str(len(allClients)) + " connected!")

        if len(allClients) == 0:
            pass
            # If this statement is true, it means both clients have disconnected and there is no client to "stop".
            # Then, clients will reconnect normally through the main listen loop and have their game states restored.

        for c in allClients:
            # there should only be one client left in this list.
            # tell this rover to stop movement until the other rover reconnects and gets the updated game info.
            c.sendall(b'{')
            c.sendall(b'"')
            c.sendall(b'd')
            c.sendall(b'i')
            c.sendall(b'r')
            c.sendall(b'"')
            c.sendall(b':')
            c.sendall(b'5')
            c.sendall(b'}')
            break

    def pingRover(self, rover, address):
        # send rover the ping signal from the server.
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'p')
        rover.sendall(b'i')
        rover.sendall(b'n')
        rover.sendall(b'g')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'1')
        rover.sendall(b'}')
        return b'{"ping":1}'

    def makeRoverMoveForward(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'd')
        rover.sendall(b'i')
        rover.sendall(b'r')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'1')
        rover.sendall(b'}')
        return b'{"dir":1}'

    def makeRoverMoveBackward(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'd')
        rover.sendall(b'i')
        rover.sendall(b'r')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'2')
        rover.sendall(b'}')
        return b'{"dir":2}'

    def makeRoverTurnLeft(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'd')
        rover.sendall(b'i')
        rover.sendall(b'r')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'3')
        rover.sendall(b'}')
        return b'{"dir":3}'

    def makeRoverTurnRight(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'd')
        rover.sendall(b'i')
        rover.sendall(b'r')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'4')
        rover.sendall(b'}')
        return b'{"dir":4}'

    def makeRoverStop(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b'd')
        rover.sendall(b'i')
        rover.sendall(b'r')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'5')
        rover.sendall(b'}')
        return b'{"dir":5}'

    def sendReconnectMessage(self, rover, address):
        rover.sendall(b'{')
        rover.sendall(b'"')
        rover.sendall(b's')
        rover.sendall(b't')
        rover.sendall(b'a')
        rover.sendall(b't')
        rover.sendall(b'"')
        rover.sendall(b':')
        rover.sendall(b'r')
        rover.sendall(b'}')
        return b'{"stat":r}'
    def sendAllMessage(self, client, message):
            allClients.add(client)
            i = 0
            print ("Start Json data sent to client: " + message)
            while (i < len(message)):
                client.sendall(message[i]);
                i = i + 1
            print ("End Json data sent to client!")
    def sendMessage(self, client, message):
            allClients.add(client)
            i = 0
            print ("Start Json data sent to client: " + message)
            while (i < len(message)):
                client.send(message[i]);
                i = i + 1
            print ("End Json data sent to client!")

    def listen(self):
        print ("Started listening for connections...")
        self.sock.listen(BACKLOG)
        while True:
            client, address = self.sock.accept()
            client.settimeout(TIMEOUT)
            threading.Thread(target = self.listenToClient,args = (client, address)).start()
    
                        
    def listenToClient(self, client, address):

        print ("Accepted connection from:", address)
        with allClients_lock:
            allClients.add(client)
            #self.pingRover(client, address)
            # if we are at this point in this function, then we know a client has connected for the first time.
            # if a client connects for the first time, we need to send the status of the game to the client that just connected.   
            # After we verify that the client has reconnected, update it with the current number of ships.

            # Send the ping message only when the rover connects for the first time / tries to reconnect.\
            data = client.recv(BUFFER_SIZE)
            print (data)
            time.sleep(2)
            global NEED_TO_RECONNECT
            NEED_TO_RECONNECT = False

        # starting time
        t = time.time()
        st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
#        print (st)
        elapsedtime = 0

        # run for 30 minutes
        while elapsedtime < 18000:
            with allClients_lock:

                try:
                    if (NEED_TO_RECONNECT):
    
                        # Send the reconnect verification only if a disconnect had occurred.
                        #self.makeOtherRoverPause(allClients)
                        # there should only be one client left in this list.
                        # tell this rover to stop movement until the other rover reconnects and gets the updated game info.
                        self.sendAllMessage(client, '{"error":5}')
                        print ("Made the other rover pause!")
                        time.sleep(1)
                        if len(allClients) == 2:
                            NEED_TO_RECONNECT = False

                    else:
                        data = ""
                        while "coordinate" not in data:
                            print("waiting for coordinate...")
                            self.sendMessage(client, '{"ping":0}')
                            data = client.recv(BUFFER_SIZE)
                            print(data)
                            print("has a coordinate?")
                        print("received")
                        count = 0
                        while count < 2:
                            if 'B' in data:
                                self.sendMessage(client, '{"hit":0}')
                            elif '4' in data:
                                self.sendMessage(client, '{"hit":0}')
                            else:
                                self.sendMessage(client, '{"miss":0}')
                            data = client.recv(BUFFER_SIZE)
                            count = count + 1
                            print (data) # recieves hello from the wifly.
                        

                except socket.error as e:
                    # There was an error in sending or receiving the data so the client probably disconnected.
                    # Alert the user about the error. The client will automatically reconnect in the main listen loop.
                    print("There was an error in sending or receiving data to client!")
                    print("Disconnecting the client...")

                    allClients.remove(client)
                    client.close()
                    print ("Client removed from:", address)
                    NEED_TO_RECONNECT = True
                    #self.makeOtherRoverPause(allClients)
                    # makeOtherRoverPause

            elapsedtime = time.time() - t
#            print (elapsedtime)

 #       print (datetime.datetime.fromtimestamp(elapsedtime).strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":

    myServer = ThreadedServer(TCP_IP, TCP_PORT)

    while True:
        myServer.listen()
