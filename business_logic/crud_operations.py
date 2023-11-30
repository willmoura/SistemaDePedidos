import sqlite3
from database.db_exceptions import DatabaseError

def create_pedido(conn, pedido):
    """
    Cria um novo pedido no banco de dados
    :param conn: Conexão com o banco de dados
    :param pedido: Uma tupla contendo informações do pedido, incluindo telefone do cliente
    """
    sql = ''' INSERT INTO Pedido_Cabecalho(NomeCliente, TelefoneCliente, DataPedido)
              VALUES(?, ?, ?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, pedido)
        conn.commit()
        return cur.lastrowid  # Retorna o ID do pedido criado
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao criar pedido: {e}")
    
def exibir_pedido(conn, pedido_id):
    """
    Visualiza os detalhes de um pedido específico
    :param conn: Conexão com o banco de dados
    :param pedido_id: ID do pedido
    """
    try:
        cur = conn.cursor()
        
        # Buscar detalhes do cabeçalho do pedido
        cur.execute("SELECT * FROM Pedido_Cabecalho WHERE ID = ?", (pedido_id,))
        pedido_cabecalho = cur.fetchone()
        if pedido_cabecalho is None:
            raise DatabaseError("Pedido não encontrado")

        # Buscar itens do pedido
        cur.execute("SELECT * FROM Pedido_Itens WHERE PedidoID = ?", (pedido_id,))
        itens_pedido = cur.fetchall()

        return {"cabecalho": pedido_cabecalho, "itens": itens_pedido}
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao visualizar pedido: {e}")

def update_pedido(conn, pedido):
    """
    Atualiza um pedido específico
    :param conn: Conexão com o banco de dados
    :param pedido: Uma tupla contendo as informações atualizadas do pedido e seu ID, incluindo telefone do cliente
    """
    sql = ''' UPDATE Pedido_Cabecalho
              SET NomeCliente = ?, TelefoneCliente = ?, DataPedido = ?
              WHERE ID = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, pedido)
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao atualizar pedido: {e}")

def delete_pedido(conn, id):
    """
    Deleta um pedido pelo ID
    :param conn: Conexão com o banco de dados
    :param id: ID do pedido
    """
    sql = 'DELETE FROM Pedido_Cabecalho WHERE ID = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao deletar pedido: {e}")