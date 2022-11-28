import socket
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from clientThread import clientThreadX


class mainWin(QMainWindow):
    client = None
    centralWidget: QWidget
    txtMessage: QTextEdit
    txtInput: QLineEdit
    userName: QLineEdit
    btnSend: QPushButton
    btnConnect: QPushButton
    isServerConnected: bool = False
    myLastMessage: str
    receivedMessage: list = ""

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        print(type(parent))
        self.myLastMessage = ""
        self.receivedMessage = []
        self.createChatLayout()
        self.initUI()
        self.clientThread = clientThreadX(self)
        self.client.sendText.connect(self.onEmitChange)

    def initUI(self):
        self.setWindowIcon(QIcon("chat.svg"))
        self.setWindowTitle("letsChat v0.0.1")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def createChatLayout(self):
        self.centralWidget = QWidget()
        inputLayout = QHBoxLayout()
        messageBoxLayout = QVBoxLayout()
        connectionLayout = QHBoxLayout()

        self.userName = QLineEdit()
        self.btnConnect = QPushButton("CONNECT")
        self.btnConnect.clicked.connect(self.connectToServer)
        connectionLayout.addWidget(self.userName)
        connectionLayout.addWidget(self.btnConnect)

        self.txtMessage = QTextEdit()
        self.txtMessage.setReadOnly(True)
        self.txtMessage.setTextColor(Qt.GlobalColor.white)
        self.txtInput = QLineEdit()
        self.txtInput.editingFinished.connect(self.onFinishedEditing)
        self.btnSend = QPushButton("SEND")
        self.btnSend.setDisabled(True)
        self.btnSend.clicked.connect(self.on_btnSend)
        inputLayout.addWidget(self.txtInput)
        inputLayout.addWidget(self.btnSend)

        messageBoxLayout.addLayout(connectionLayout)
        messageBoxLayout.addWidget(self.txtMessage)
        messageBoxLayout.addLayout(inputLayout)
        self.centralWidget.setLayout(messageBoxLayout)
        self.setCentralWidget(self.centralWidget)

    def connectToServer(self):
        if not self.isServerConnected and self.userName.text() != "":
            self.setClientEnable(True)
            if ok := self.client.callServer():
                print("connected")
        else:
            self.setClientEnable(False)

    def setClientEnable(self, trueOrFalse):
        # sourcery skip: extract-duplicate-method
        if trueOrFalse:
            self.btnConnect.setText("disCONNECT")
            self.btnSend.setEnabled(True)
            self.txtInput.setEnabled(True)
            self.userName.setEnabled(False)
            self.isServerConnected = True
        else:
            self.btnConnect.setText("CONNECT")
            self.btnSend.setEnabled(False)
            self.txtInput.setEnabled(False)
            self.userName.setEnabled(True)
            self.isServerConnected = False

    def onEmitChange(self, message):
        try:
            if message != "" or message is not None:
                messageRcv = message.split("::::")
                for x in messageRcv:
                    self.txtMessage.append(x)
                print(message)
        except Exception as e:
            print("there was an error receiving messages")
            print(e)

    def sendMessage(self, message):
        """
        send a message to the server to be broadcast
        :return:
        """
        if message == 'quit':
            quitMsg = f"{self.userName.text()} :::: I'm quitting the chat. See you!"
            self.client.client.send(quitMsg.encode('UTF-8'))
            self.client.client.close()
        else:
            sendMesg = f"{message}"
            self.client.client.send(sendMesg.encode('utf-8'))



    def __exit__(self, exc_type, exc_val, exc_tb):
        self.setClientEnable(False)
        QApplication.instance().quit()

    def on_btnSend(self):
        message = self.txtInput.text().replace("\n", "")
        self.myLastMessage = message
        self.txtInput.clear()
        self.sendMessage(message)

    def onFinishedEditing(self):
        message = self.txtInput.text()
        self.myLastMessage = message
        self.txtInput.clear()
        self.sendMessage(message)






def main():
    app = QApplication([])
    ex = mainWin()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
