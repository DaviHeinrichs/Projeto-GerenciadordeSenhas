import random #biblioteca que gera dados aleatórios
import string #biblioteca que contém lista de caracteres prontos

def generate_pass(tamanho):
    carac = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(carac) for _ in range(tamanho))
    return password


print(generate_pass(12))