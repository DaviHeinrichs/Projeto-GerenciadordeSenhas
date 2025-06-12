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
from utils.telas.ui_generatePassword_window import Ui_generatePassword_window
from utils.telas.ui_boasVindas_window import Ui_boasvindas_window
from utils.telas.ui_createMasterPassword_window import Ui_createmaster_window
from utils.telas.ui_checkPassword_window import Ui_checkPassword_window
from utils.telas.ui_SafeMenu_window import Ui_safemenu_window
from utils.telas.ui_DescptPass_window import Ui_decrypt_window
from utils.telas.ui_myPassword_window import Ui_myPassword_window
from utils.telas.ui_SenhaNCadastrada_window import Ui_createpass_window
from utils.telas.ui_createPassword_window import Ui_passcreate_window
from utils.telas.ui_Admin_window import ui_Admin_window



class tela_admin(QDialog):
    def __init__(self,*args,**argvs):
        super(tela_admin,self).__init__(*args,**argvs)
        self.ui = ui_Admin_window()
        self.ui.setupUi(self)
        self.ui.sair.clicked.connect(self.voltar)
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import load_user_table
        
        dados, User_table = load_user_table()
        
        headers = [col.name for col in User_table.columns]
        model = self.create_table_model(data=dados, headers=headers)
        self.ui.Tabela.setModel(model)
        
    def create_table_model(self, data, headers):
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        
        model.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, col in enumerate(headers):
                model.setItem(i, j, QStandardItem(str(getattr(row, col))))
        
        return model
    def voltar(self):
        self.hide()
        self.tela_l = login()
        self.tela_l.show()
        
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
        from interface.users.user_data.statements.main import check_login, have_masterpassword, get_role_id
        
        email = self.ui.emailInput.text()
        senha = self.ui.senhaInput.text()
        if check_login(email,senha) == True:
            if get_role_id(user_email=email) == 1:
                if have_masterpassword(email) == True:
                    self.hide()
                    self.tela_p = tela_principal_user(remail=email)
                    self.tela_p.show()
                
                elif have_masterpassword(email) == False:
                    self.hide()
                    self.tela_m = criar_masterpassword(remail=email)
                    self.tela_m.show()
                else:
                    mostrar_erro("Erro no Login!","Ocorreu um erro inesperado!")
            elif get_role_id(user_email=email) == 2:
                self.hide()
                self.tela_admin = tela_admin()
                self.tela_admin.show()
        elif check_login(email,senha) == False:
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
            self.hide()
            self.tela_p = tela_principal_user(remail=self.email)
            self.tela_p.show()
                  
    def voltar_login(self):
        self.hide()
        self.tela_l = login()
        self.tela_l.show()
        
    def tela_gerar(self):
        self.tela_g = tela_gerar()
        self.tela_g.show()

class tela_cofre(QDialog):
    def __init__(self,remail,*args,**argvs):
        super(tela_cofre,self).__init__(*args,**argvs)
        self.ui = Ui_safemenu_window()
        self.ui.setupUi(self)
        self.email = remail
        self.ui.passwd1Button.clicked.connect(self.senha1)
        self.ui.passwd2Button.clicked.connect(self.senha2)
        self.ui.passwd3Button.clicked.connect(self.senha3)
        self.ui.passwd4Button.clicked.connect(self.senha4)
        self.ui.passwd5Button.clicked.connect(self.senha5)
        self.ui.exit.clicked.connect(self.voltar)
        self.ui.exit_2.clicked.connect(self.sair)
    
    def senha1(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import não_tem_senha1
        
        if não_tem_senha1(self.email) == True:
            self.hide()
            self.confirm = confirm_create(senha="pass1", remail=self.email) 
            self.confirm.show()
        elif não_tem_senha1(self.email) == False:
            self.hide()
            self.tela_dec = decrypto_senha(senha="pass1", remail=self.email)
            self.tela_dec.show()
            
    def senha2(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import não_tem_senha2
        
        if não_tem_senha2(self.email) == True:
            self.hide()
            self.confirm = confirm_create(senha="pass2", remail=self.email)
            self.confirm.show() 
        elif não_tem_senha2(self.email) == False:
            self.hide()
            self.tela_dec = decrypto_senha(senha="pass2", remail=self.email)
            self.tela_dec.show()
    
    def senha3(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import não_tem_senha3
        
        if não_tem_senha3(self.email) == True:
            self.hide()
            self.confirm = confirm_create(senha="pass3", remail=self.email)
            self.confirm.show() 
        elif não_tem_senha3(self.email) == False:
            self.hide()
            self.tela_dec = decrypto_senha(senha="pass3", remail=self.email)
            self.tela_dec.show()
    
    def senha4(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import não_tem_senha4
        
        if não_tem_senha4(self.email) == True:
            self.hide()
            self.confirm = confirm_create(senha="pass4", remail=self.email)
            self.confirm.show() 
        elif não_tem_senha4(self.email) == False:
            self.hide()
            self.tela_dec = decrypto_senha(senha="pass4", remail=self.email)
            self.tela_dec.show()
            
    def senha5(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import não_tem_senha5
        
        if não_tem_senha5(self.email) == True:
            self.hide()
            self.confirm = confirm_create(senha="pass5", remail=self.email)
            self.confirm.show() 
        elif não_tem_senha5(self.email) == False:
            self.hide()
            self.tela_dec = decrypto_senha(senha="pass5", remail=self.email)
            self.tela_dec.show()        
            
        
    def sair(self):
        self.hide()
        self.tela_l = login()
        self.tela_l.show()
                    
    def voltar(self):
        self.hide()
        self.tela_p = tela_principal_user(self.email)
        self.tela_p.show()

class confirm_create (QDialog):
    def __init__(self,senha,remail,*args,**argvs):
        super(confirm_create,self).__init__(*args,**argvs)
        self.ui = Ui_createpass_window()
        self.ui.setupUi(self)
        self.senha = senha
        self.email = remail
        self.ui.exit.clicked.connect(self.voltar)
        self.ui.exit_2.clicked.connect(self.entrar)
        
    def entrar(self):
        self.hide()
        self.tela_criar = new_password(senha=self.senha,remail=self.email)
        self.tela_criar.show()
        
    def voltar(self):
        self.hide()
        self.tela_cofre = tela_cofre(remail=self.email)
        self.tela_cofre.show()
        
class new_password(QDialog):
    def __init__(self,senha,remail,*args,**argvs):
        super(new_password,self).__init__(*args,**argvs)
        self.ui = Ui_passcreate_window()
        self.ui.setupUi(self)
        self.senha = senha
        self.email = remail
        self.ui.Create.clicked.connect(self.registrar_senha)
        self.ui.generateNewPasswordBtn.clicked.connect(self.gerar)
        self.ui.exit.clicked.connect(self.voltar)
        
    def voltar(self):
        self.hide()
        self.tela_cofre = tela_cofre(remail=self.email)
        self.tela_cofre.show()
        
    def gerar(self):
        self.tela_g = tela_gerar()
        self.tela_g.show()
        
    def registrar_senha(self):
        from utils.erro_comum import mostrar_erro
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import criar_senha
        senha_digitada = self.ui.senhaInput.text()
        local_digitado = self.ui.nomeSenhaInput.text()
        confirme_senha = self.ui.ConfirmaSenhaInput.text()
        
        if senha_digitada == confirme_senha:
            criar_senha(self.senha,self.email,senha_digitada,local_digitado)
            self.hide()
            self.tela_cofre = tela_cofre(remail=self.email)
            self.tela_cofre.show()
        else:
            mostrar_erro("Erro no registro da nova senha!","Senhas digitadas são diferentes!!")
        
class decrypto_senha(QDialog):
    def __init__(self,senha,remail,*args,**argvs):
        super(decrypto_senha,self).__init__(*args,**argvs)
        self.ui = Ui_decrypt_window()
        self.ui.setupUi(self)
        self.senha = senha
        self.email = remail
        self.ui.revelar.clicked.connect(self.revelar)
        self.tentativas = 5
        
    def revelar(self):
        from utils.erro_comum import mostrar_erro
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from interface.users.user_data.statements.main import get_senha, verificar_master
        senha_inserida = self.ui.senhaMasterInput.text()
        
        verify = verificar_master(senha_inserida, self.email)    
        if verify == True:
            user_senha, onde_usada = get_senha(self.senha,self.email)
            self.hide()
            self.tela_my = my_password(self.email,user_senha,onde_usada)
            self.tela_my.show()
        else:   
            self.tentativas -= 1 
            if self.tentativas > 0:
                mostrar_erro("Erro ao mostrar senha!!", f"MASTERPASSWORD INCORRETA!\nVocê possui mais {self.tentativas} tentativas!")
            else:
                mostrar_erro("VOCÊ NÃO POSSUI MAIS TENTATIVAS!", "Tente novamente mais tarde!")
                self.close()
        
class my_password(QDialog):
    def __init__(self,remail,senha,onde_usada,*args,**argvs):
        super(my_password,self).__init__(*args,**argvs)
        self.ui = Ui_myPassword_window()
        self.ui.setupUi(self)
        self.email = remail
        self.ui.show_senha.setPlainText(f"{senha}")
        self.ui.show_where.setPlainText(f"{onde_usada}")
        self.ui.exit.clicked.connect(self.voltar_cofre)
        self.ui.exit_2.clicked.connect(self.voltar_principal)
        
    def voltar_principal(self):
        self.hide()
        self.tela_p = tela_principal_user(remail=self.email)
        self.tela_p.show()
        
    def voltar_cofre(self):
        self.hide()
        self.tela_cofre = tela_cofre(remail=self.email)
        self.tela_cofre.show()
                         
class tela_principal_user(QDialog):
    def __init__(self,remail,*args,**argvs):
        super(tela_principal_user,self).__init__(*args,**argvs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.email = remail
        self.ui.generateNewPasswordBtn.clicked.connect(self.tela_gerar)
        self.ui.myPasswordsButton.clicked.connect(self.cofre)
        self.ui.comoEstaMinhaPass.clicked.connect(self.senha_forte)
        self.ui.exit.clicked.connect(self.sair)
        
    def sair(self):
        self.hide()
        self.tela_l = login()
        self.tela_l.show()
            
    def senha_forte(self):
        self.hide()
        self.tela_f = tela_senha_forte(self.email)
        self.tela_f.show()
        
    def cofre(self):
        self.hide()
        self.tela_cofre = tela_cofre(remail=self.email)
        self.tela_cofre.show()
        
    
    def tela_gerar(self):
        self.tela_gen = tela_gerar()
        self.tela_gen.show()
        

class tela_senha_forte(QDialog):
    def __init__(self,remail,*args,**argvs):
        super(tela_senha_forte, self).__init__(*args,**argvs)
        self.ui = Ui_checkPassword_window()
        self.ui.setupUi(self)
        self.email = remail
        self.ui.checkPassButton.clicked.connect(self.checar)
        self.ui.exit.clicked.connect(self.voltar)
        
    def checar(self):
        from utils.erro_comum import mostrar_erro, mostrar_informacao
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bin')))
        from utils.password_functions.validate_pass.main import check_havebeenpwned, password_validation
        
        password = self.ui.senhaInput.text()
        
        mensagem, valida, score = password_validation(password)
        
        if not password.strip():
            mostrar_erro("Digite uma senha!!!", f"Você deve digitar uma senha para ser verificada!!")  
        else:
            if check_havebeenpwned(password) == False:
                if valida:
                    mostrar_informacao("Sua senha é forte!", f"Sua senha NÃO está vazada na internet, PARABÉNS!\n\n{mensagem}\nSeu Score é de {score}/5")
                elif not valida:
                    mostrar_erro("Sua senha falha no nosso Validador!", f"Sua senha NÃO está vazada na internet!\n\nProblemas encontrados:\n{mensagem}\nSeu Score é de {score}/5")  
            elif check_havebeenpwned(password) == True:
                mostrar_erro("Sua senha está vazada!", "Sua senha pode estar vazada segundo o Have I Been Pwned\nCheque o site https://haveibeenpwned.com/ para mais informações!")  
            else:
                mostrar_erro("Erro de conexão", "Não foi possível verificar vazamentos. Tente novamente.")
    
    def voltar(self):
        self.hide()
        self.tela_p = tela_principal_user(self.email)
        self.tela_p.show()        

            
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