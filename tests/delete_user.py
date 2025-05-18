import sqlite3

def delete_user(user_name):
    conn = sqlite3.connect("nomedobanco.db")
    cursor = conn.cursor

    cursor.execute("DELETE FROM nomedatabela WHERE nome = ?", (user_name))

    conn.commit()
    conn.close()
    print(f"Usuário '{user_name}' apagado com sucesso!")