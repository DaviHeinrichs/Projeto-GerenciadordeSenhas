from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

from utils.telas.login_tela import Ui_LoginWindow
from utils.telas.ui_cadastro_window import Ui_CadastroWindow
from utils.telas.ui_mainmenu_window import Ui_MainWindow

class login(QDialog):
    def __init__(self,*args,**argvs):
        super(login,self).__init__(*args,**argvs)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.entrarButton.clicked.connect(self.entrar)
        self.ui.cadastroButton.clicked.connect(self.tela_cadastro)
    
    def entrar(self):
        #Checa os campos
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        
        if not email.strip():
            self.mostrar_erro("Erro no Login!","Email necessário!")
            self.ui.emailInput.setFocus()
            return
        
        if not senha.strip():
            self.mostrar_erro("Erro no Login!","Senha necessária!")
            self.ui.senhaInput.setFocus()
            return
        
        def abrir_principal(self):
            self.hide()
            self.tela_p = tela_principal_user()
            self.tela_p.show()
        abrir_principal(self)
        
        
        
    def mostrar_erro(self, titulo, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.exec_()
        
        
        
    
    def tela_cadastro(self):
        self.tela = cadastrar_tela()
        self.tela.show()
        
        
class tela_principal_user(QDialog):
    def __init__(self,*args,**argvs):
        super(tela_principal_user,self).__init__(*args,**argvs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
                
        
            
class cadastrar_tela(QDialog):
    def __init__(self,*args,**argvs):
        super(cadastrar_tela,self).__init__(*args,**argvs)
        self.ui = Ui_CadastroWindow()
        self.ui.setupUi(self)
        self.ui.cadastrarseButton.clicked.connect(self.cadastrar)
        
    def cadastrar(self):
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        confirme_senha = self.ui.senha2Input.text()
        nome = self.ui.nameInput.text() 
        sobrenome = self.ui.lastnameInput.text()
        
        #checando as caixas
        if not email.strip():
            self.mostrar_erro("Erro no Cadastro!","Email necessário!")
            self.ui.emailInput.setFocus()
            return
        
        if not senha.strip():
            self.mostrar_erro("Erro no Cadastro!","Senha vazia!")
            self.ui.senhaInput.setFocus()
            return
        
        if not confirme_senha.strip():
            self.mostrar_erro("Erro no Cadastro!","Você deve confirmar sua senha!")
            self.ui.senha2Input.setFocus()
            return
        
        if not nome.strip():
            self.mostrar_erro("Erro no Cadastro!","Nome Sobrenome necessários!")
            self.ui.nameInput.setFocus()
            return
        
        if not sobrenome.strip():
            self.mostrar_erro("Erro no Cadastro!","Nome Sobrenome necessários!")
            self.ui.lastnameInput.setFocus()
            return
         
        #checando email
        if ("@" and ".com") in email:
           return print("boa")
        elif (" ") in email:
            self.mostrar_erro("Erro no Cadastro!", "O email não pode conter espaços!")
            self.ui.emailInput.selectAll()
            self.ui.emailInput.setFocus()
            return
        else:
            self.mostrar_erro("Erro no Cadastro!", "Formato de Email Incorreto!")
            self.ui.emailInput.selectAll()
            self.ui.emailInput.setFocus()
            return
        
        
        
    def mostrar_erro(self, titulo, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.exec_()
        
app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = login()
    window.show()
sys.exit(app.exec_()) 