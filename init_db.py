import sqlite3

def init_db():
    with open('schema.sql', 'r') as f:
        schema = f.read()

    conn = sqlite3.connect('C:/Users/bruno/OneDrive/Documentos/Python_Projects/Facul/LW/project_web/instance/db.sqlite')  # ou o caminho do seu banco
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco criado com sucesso!")
