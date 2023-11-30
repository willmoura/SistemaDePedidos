import sqlite3
import json
from tkinter import messagebox

def create_connection(db_file=None):
    """ 
    Cria uma conexão com o banco de dados SQLite.
    :param db_file: Caminho do arquivo de banco de dados ou ':memory:' para banco de dados em memória.
    """
    if db_file is None:
        try:
            # Carrega a configuração do arquivo JSON
            with open('config.json', 'r') as f:
                config = json.load(f)
            db_file = config['database_path']
        except FileNotFoundError:
            messagebox.showerror("Erro de Configuração", "Arquivo config.json não encontrado")
            return None
        except KeyError:
            messagebox.showerror("Erro de Configuração", "Caminho do banco de dados não definido em config.json")
            return None
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
    return conn