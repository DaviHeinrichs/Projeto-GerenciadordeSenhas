import sqlite3

def adicionar_usuario(user_name, password):
    conn = sqlite3.connect("nomedobanco.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO nomedatabela (nome, senha) VALUES (?, ?)", (user_name, password))

    conn.commit()
    conn.close()

    print(f"Usuário '{user_name}' adicionado com sucesso!")
