from PyQt5.QtWidgets import *

def mostrar_erro(titulo, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.exec_()
        
def mostrar_informacao(titulo, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.exec_()
        