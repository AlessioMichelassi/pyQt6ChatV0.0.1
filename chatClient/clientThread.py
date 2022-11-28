import socket
import sys
import threading
from threading import Thread
import socket
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

version = "0.0.1"
author = "Alessio Michelassi"

ipv4Protocol = socket.AF_INET
tcpProtocol = socket.SOCK_STREAM

hostName = socket.gethostname()
HOST_IP = socket.gethostbyname(hostName)
HOST_PORT: int = 12346
ENCODER = 'utf-8'
BYTE_SIZE = 1024


class clientThreadX(QObject):
    client: socket
    isServerConnected: bool = False
    sendText = pyqtSignal(str)
    winApp = None
    thread1: threading

    def __init__(self, chatGui):
        super(clientThreadX, self).__init__()
        self.winApp = chatGui
        self.thread1 = threading.Thread(target=self.receiveMessage)
        self.winApp.client = self

    def callServer(self):
        try:
            self.client = socket.socket(ipv4Protocol, tcpProtocol)
            self.client.connect((HOST_IP, HOST_PORT))
            self.winApp.setClientEnable(True)
            self.thread1.start()
            return True
        except Exception as e:
            a = e
            self.sendText.emit("[SYSTEM] server down")
            self.winApp.setClientEnable(False)
            return False

    def receiveMessage(self):
        while True:
            try:
                message = self.client.recv(BYTE_SIZE).decode(ENCODER)
                if message.startswith('[Server]'):
                    if message == '[Server] NAME':
                        name = self.winApp.userName.text().encode('utf-8')
                        self.client.send(name)
                else:
                    self.sendText.emit(message)
                    print(f"message from thread: {message}")

            except Exception as e:
                self.sendText.emit("an error occurred...")
                self.sendText.emit(str(e))
                break
        self.client.close()
