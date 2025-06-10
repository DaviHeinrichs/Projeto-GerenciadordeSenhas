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
from utils.telas.ui_mainmenu_windowNEW import Ui_MainWindow
from utils.telas.ui_generatePassword_window import Ui_generatePassword_window
from utils.telas.ui_boasVindas_window import Ui_boasvindas_window
from utils.telas.ui_createMasterPassword_window import Ui_createmaster_window

class login(QDialog):
    def __init__(self,*args,**argvs):
        super(login,self).__init__(*args,**argvs)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.entrarButton.clicked.connect(self.entrar)
        self.ui.cadastroButton.clicked.connect(self.tela_cadastro)
    
    def entrar(self):
        from utils.erro_comum import mostrar_erro 
        #Checa os campos
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        
        if not email.strip():
            mostrar_erro("Erro no Login!","Email necessário!")
            self.ui.emailInput.setFocus()
            return
        elif not senha.strip():
            mostrar_erro("Erro no Login!","Senha necessária!")
            self.ui.senhaInput.setFocus()
            return
        else:
            self.ui.entrarButton.clicked.connect(self.tentar_logar)
            
    def tentar_logar(self):
        from utils.erro_comum import mostrar_erro
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import check_login, have_masterpassword
        
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        if check_login(email,senha) == True:
            if have_masterpassword(email) == True:
                self.hide()
                self.tela_p = tela_principal_user()
                self.tela_p.show()
                print("bemvindo")
            elif have_masterpassword(email) == False:
                self.hide()
                self.tela_m = criar_masterpassword(remail=email)
                self.tela_m.show()
                return email
            else:
                mostrar_erro("Erro no Login!","Ocorreu um erro inesperado!")
                
        if check_login(email,senha) == False:
            self.hide()
            mostrar_erro("Erro no Login!","Email ou Senha incorretos!")
            self.tela_l = login()
            self.tela_l.show()
        
        
    def tela_cadastro(self):
        self.hide()
        self.tela = cadastrar_tela()
        self.tela.show()

class criar_masterpassword(QDialog):
    def __init__(self,remail,*args,**argvs):
        super(criar_masterpassword,self).__init__(*args,**argvs)
        self.ui = Ui_createmaster_window()
        self.email = remail
        self.ui.setupUi(self)
        self.ui.generateNewPasswordBtn.clicked.connect(self.tela_gerar)
        self.ui.exit.clicked.connect(self.voltar_login)
        self.ui.Create.clicked.connect(self.create_master)
        
    def create_master(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import get_salt, get_id, criar_masterpassword, turn_havemaster
        user_salt = get_salt(self.email)
        user_id = get_id(self.email)
        senha = self.ui.senhaInput.text()
        confirme_senha = self.ui.ConfirmaSenhaInput.text()
        
        if senha == confirme_senha:
            criar_masterpassword(senha, user_salt, user_id)    
            turn_havemaster(user_id)
            print("masterpassword gerada")
            self.hide()
            self.tela_p = tela_principal_user()
            self.tela_p.show()
        
        
        
        
         
    def voltar_login(self):
        self.hide()
        self.tela_l = login()
        self.tela_l.show()
        
    def tela_gerar(self):
        self.tela_g = tela_gerar()
        self.tela_g.show()
    
    


        
        
class tela_principal_user(QDialog):
    def __init__(self,*args,**argvs):
        super(tela_principal_user,self).__init__(*args,**argvs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.generateNewPasswordBtn.clicked.connect(self.tela_gerar)
    
    def tela_gerar(self):
        self.tela_gen = tela_gerar()
        self.tela_gen.show()
        
            
class tela_gerar(QDialog):
    def __init__(self,*args,**argvs):
        super(tela_gerar,self).__init__(*args,**argvs)
        self.ui = Ui_generatePassword_window()
        self.ui.setupUi(self)
        self.ui.newPasswordButton.clicked.connect(self.gerar)
        self.ui.exit.clicked.connect(self.voltar)
        
    def gerar(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from utils.password_functions.gen_sequency.main import gen_sequency, sequency_mixer
        sbeta = gen_sequency()
        senha = sequency_mixer(sbeta)
            
        self.ui.senhaOutput.setText(str(senha))
    
    def voltar(self):
        self.hide()
                
            
class cadastrar_tela(QDialog):
    def __init__(self,*args,**argvs):
        super(cadastrar_tela,self).__init__(*args,**argvs)
        self.ui = Ui_CadastroWindow()
        self.ui.setupUi(self)
        self.ui.cadastrarseButton.clicked.connect(self.checar_caixa)    
    
    def checar_caixa(self):
        from utils.erro_comum import mostrar_erro
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        confirme_senha = self.ui.senha2Input.text()
        nome = self.ui.nameInput.text() 
        sobrenome = self.ui.lastnameInput.text()
        
        #checando as caixas
        if not email.strip():
            mostrar_erro("Erro no Cadastro!","Email necessário!")
            self.ui.emailInput.setFocus()
            return
        
        if not senha.strip():
            mostrar_erro("Erro no Cadastro!","Senha vazia!")
            self.ui.senhaInput.setFocus()
            return
        
        if not confirme_senha.strip():
            mostrar_erro("Erro no Cadastro!","Você deve confirmar sua senha!")
            self.ui.senha2Input.setFocus()
            return
        
        if not nome.strip():
            mostrar_erro("Erro no Cadastro!","Nome Sobrenome necessários!")
            self.ui.nameInput.setFocus()
            return
        
        if not sobrenome.strip():
            mostrar_erro("Erro no Cadastro!","Nome Sobrenome necessários!")
            self.ui.lastnameInput.setFocus()
            return
        if ("@" and ".com") in email:
            self.ui.cadastrarseButton.clicked.connect(self.cadastrar)
        elif (" ") in email:
            mostrar_erro("Erro no Cadastro!", "O email não pode conter espaços!")
            self.ui.emailInput.selectAll()
            self.ui.emailInput.setFocus()
            return
        elif not(("@" and ".com") in email):
            mostrar_erro("Erro no Cadastro!", "Formato do email incorreto!")
            self.ui.emailInput.selectAll()
            self.ui.emailInput.setFocus()
            return
        else:
            self.cadastrar
 
    def cadastrar(self):
        from utils.erro_comum import mostrar_erro
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import criar_user, check_user
        
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        confirme_senha = self.ui.senha2Input.text()
        nome = self.ui.nameInput.text() 
        sobrenome = self.ui.lastnameInput.text()
        
        if (check_user(email) == True) and (senha == confirme_senha):
            criar_user(nome,sobrenome,email,senha)
            self.hide()
            self.tela_gen = boas_vindas()
            self.tela_gen.show()
            return
        
        elif check_user(email) == False:
            self.hide()
            mostrar_erro("Erro no Cadastro!", "O email já foi utilizado!")
            self.tela = cadastrar_tela()
            self.tela.show()
            
        elif senha != confirme_senha:
            mostrar_erro("Erro no Cadastro!", "As senhas são diferentes")
            self.ui.senhaInput.setFocus()
            return
        else:
            mostrar_erro("Erro no Cadastro!", "Ocorreu um erro inesperado... Tente novamente!")
            return       

class boas_vindas(QDialog):
    def __init__(self,*args,**argvs):
        super(boas_vindas,self).__init__(*args,**argvs)
        self.ui = Ui_boasvindas_window()
        self.ui.setupUi(self)
        self.ui.exit.clicked.connect(self.voltar_login)
        
    def voltar_login(self):
        self.hide()
        self.vol_login = login()
        self.vol_login.show()
                     
app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = login()
    window.show()
sys.exit(app.exec_()) 