import re
import requests
import hashlib

def password_validation(used_senha):
    minuscula = re.search(r'[a-z]', used_senha)
    maiuscula = re.search(r'[A-Z]', used_senha)
    digito = re.search(r'[0-9]', used_senha)
    especial = re.search(r'[^a-zA-Z0-9]', used_senha)
        
    score = 0
    problemas = []
    
    if especial:
        score+=1
    else:
        problemas.append("Senha não possui Caracteres Especiais!")
    if maiuscula:
        score+=1
    else:
        problemas.append("Senha não possui Letra Maiúscula!")
    if minuscula:
        score+=1
    else:
        problemas.append("Senha não possui Letra Minúscula!")
    if digito:
        score+=1
    else:
        problemas.append("Senha não possui digitos!")
        
    if len(used_senha)>= 12:
        score+=1
    else:
        problemas.append("Senha possui menos que 12 caracteres!")
    
    if not problemas:
        return "Sua senha preenche os requisitos mínimos!",True, score
    

    resultado_simples = "\n".join(problemas)
    return resultado_simples, False, score
        
    
def check_havebeenpwned(used_senha):
    sha1_hash = hashlib.sha1(used_senha.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code != 200:
        raise RuntimeError("Erro ao acessar a API do Have I Been Pwned")

    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return True  
    return False  
        