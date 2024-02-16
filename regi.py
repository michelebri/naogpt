import socket
import qi
import argparse
import sys
import time
import numpy as np
import socket

class SoundProcessingModule(object):

    def __init__( self,app):
        self.stopAcquire = False
        self.needAcquisition = True
        self.audioBuffer = []
        self.acquire = True
        self.app = app
        super(SoundProcessingModule, self).__init__()
        self.app.start()
        self.module_name = "SoundProcessingModule"

    def stopProcessing(self):
        self.needAcquisition= False
        self.audio_service.unsubscribe(self.module_name)

    def startProcessing(self):
        self.needAcquisition = True
        self.audioBuffer = []
        session = self.app.session
        self.audio_service = session.service("ALAudioDevice")
        # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
        self.audio_service.setClientPreferences("SoundProcessingModule", 16000, 3, 0)
        self.audio_service.subscribe(self.module_name)
    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):

        if (self.needAcquisition):
            self.audioBuffer.extend(inputBuffer)
            print("acqusition")
            print(len(self.audioBuffer))



        
def start_server(ip, port):
    try:
	# Initialize qi framework.
       connection_url = "tcp://" + ip + ":" + str(9559)
       app = qi.Application(["SoundProcessingModule", "--qi-url=" + connection_url])
       MySoundProcessingModule = SoundProcessingModule(app)
       app.session.registerService("SoundProcessingModule", MySoundProcessingModule)

     
    except RuntimeError:

      sys.exit(1)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((ip, port))
    serversocket.listen(1)  # Accepts only one connection at a 

    print("Server listening on {}:{}".format(ip, port))

    while True:
        client_socket, address = serversocket.accept()
        print("Connection from", address)

        try:
            while True:
                command = client_socket.recv(1024).strip().lower()
                if command == b"start":
                     MySoundProcessingModule.startProcessing()
                     print("sto a registranre")
                elif command == b"size":
                    MySoundProcessingModule.stopProcessing()
                    client_socket.sendall(str(len(MySoundProcessingModule.audioBuffer)).encode('utf-8'))
                elif command == b"audio":    
                    audio_bytes = bytearray(MySoundProcessingModule.audioBuffer)
                    client_socket.sendall(audio_bytes)
                elif not command:
                    break  # Break the loop if the client 
        finally:
            client_socket.close()

# Set up NAOqi components
ip = "10.42.0.89"
start_server(ip, 4352)  # Replace "NAO_IP" with the 


