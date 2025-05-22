import secrets
import random
import string

master_password = 'Heinrich@2612'

def mix_master(master_paswword):
    master_list = list(master_password)
    random.shuffle(master_list)
    return ''.join(master_list)

mixed = mix_master(master_password)    
    
def gerar_chave_aes(mixed):
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%&"
    key = list(mixed)
    for s in ):
        senha+=(secrets.choice(options))
        senha_max +=1
    

    chave_embaralhada = chave_embaralhada.ljust(32)[:32].encode()  # Padding/truncamento
    return chave_embaralhada

print(gerar_chave_aes(master_password))