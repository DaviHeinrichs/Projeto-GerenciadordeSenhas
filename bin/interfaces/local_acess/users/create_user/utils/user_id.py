import secrets
import string

def id_gen():
    id = []
    contador = 1
    
    while contador <=4:
        options = string.digits
        id+=secrets.choice(options)
        contador+=1

    id_string = ''.join(id)
    
    return int(id_string)

id_nova = id_gen()

print(type(id_nova))
print(id_nova)