import sqlite3

def add_pas(user_name, password):
    conn = sqlite3.connect("nomedobanco.db") #precisa alterar aqui
    cursor = conn.cursor()

    cursor.execute("INSERT INTO nomedatabela (coluna1,coluna2) VALUES (?, ?)", (user_name, password))

    conn.commit()
    conn.close()

    print("Usuário adicionado com sucesso!")