import socket
import threading
from datetime import datetime

ipv4Protocol = socket.AF_INET
tcpProtocol = socket.SOCK_STREAM

hostName = socket.gethostname()
HOST_IP = socket.gethostbyname(hostName)
HOST_PORT: int = 12346
ENCODER = 'utf-8'
BYTE_SIZE = 1024

server = socket.socket(ipv4Protocol, tcpProtocol)

# server.close()
server.bind((HOST_IP, HOST_PORT))
server.listen()

clientSocketList = []
clientNameList = []
lastMessage = ""

def broadcast(message, name, currentClient):
    """
    send a message to all client connected
    :param currentClient: current client
    :param name: name of the current client
    :param message: the message to send
    :return:
    """
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
    print("*" * 30)

    for client in clientSocketList:
        if client != currentClient:
            index = clientSocketList.index(client)
            currentName = clientNameList[index]
            print(f"message broadcasted to: {currentName} ")
            msgToSend = f"{currentTime}::::{name} said: ::::{message}"
            print(msgToSend)
            client.send(msgToSend.encode(ENCODER))
    print("*" * 30)


def sendPersonalMessage(message, name, client):
    """
    Quando un client manda un messaggio a tutti. Il server
    si occupa di prendere il messaggio e lo manda a tutti tranne a chi l'ha mandato.
    nel caso in cui il server deve mandare un messaggio a un solo
    destinatario usa questa funzione
    :param message: il messaggio da inviare
    :param client: il socket del cliet
    :return: nulla
    """
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
    messageFromServer = f"{currentTime}::::[SERVER] said: ::::{message}"
    client.send(messageFromServer.encode(ENCODER))
    print(messageFromServer)


def receiveMessage(_clientSocket):
    """
    Il server riceve il messaggio da un certo client
    e con la funzione broadcast lo manda a tutti gli altri client collegati
    :return:
    """
    while True:
        try:
            index = clientSocketList.index(_clientSocket)
            name = clientNameList[index]
            message = _clientSocket.recv(BYTE_SIZE).decode(ENCODER)
            if message != lastMessage:
                # messageToSend = f"\033[1;92m\t{name}: {message}\033[0m"
                print("*"*30)
                print("received message:")
                print(message)
                print("*" * 30)
                broadcast(message, name, _clientSocket)
                lastMessage = message
        except Exception:
            # Find the index of the client socket in our list
            index = clientSocketList.index(_clientSocket)
            name = clientNameList[index]

            # Remove the client socket and name from lists
            clientSocketList.remove(_clientSocket)
            clientNameList.remove(name)
            # broadcast(f"\033[5;91m\t{name} has left the chat\033[0m")
            broadcast(f"[SERVER] {name} has left the chat", name, _clientSocket)
            _clientSocket.close()
            break


def connectClient():
    """
    connect an incoming client to the server
    :return:
    """
    while True:
        clientSocket, clientAddress = server.accept()
        try:
            # accept any incoming connection
            print(f"connected with: {clientAddress}...")
            # in questa parte il server si occupa dell'accettazione del client
            # il client fornisce un nome in automatico
            # appena il server gli manda il messaggio [Server] NAME
            clientSocket.send("[Server] NAME".encode(ENCODER))
            clientName = clientSocket.recv(BYTE_SIZE).decode(ENCODER)
            # aggiunge il lient au una lista di client e di nomi
            clientSocketList.append(clientSocket)
            clientNameList.append(clientName)
            print(f"name of the new Client: {clientName}")
            # risponde in maniera privata al client:
            msg = f"{clientName} welcome to the chat."
            sendPersonalMessage(msg, clientName, clientSocket)
            # avverte tutti i partecipanti alla chat che questo è entrato
            broadcast(f"[Server] {clientName} just join the chat", clientName, clientSocket)
            receiveThread = threading.Thread(target=receiveMessage, args=(clientSocket,))
            receiveThread.start()
        except Exception as e:
            print("+" * 30)
            print(e)
            index = clientSocketList.index(clientSocket)
            name = clientNameList[index]
            clientSocketList.remove(clientSocket)
            print(f"{name} has gone to to this error...")
            clientNameList.remove(name)
            clientSocket.close()
            print("+" * 30)
            connectClient()
            print("server is waiting from incoming connection....")



print("server is waiting from incoming connection....")
connectClient()
